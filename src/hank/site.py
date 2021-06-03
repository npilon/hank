"""A Work Site is configured with a dispatcher to perform work from
a specified set of queues.

Most Work Sites can only accept specific types of queues,
and will raise an exception if asked to acquire tasks of unexpected types.
"""

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from itertools import groupby
import random
from typing import Optional

import redis

from .dispatcher import Dispatcher
from .work_queue import WorkQueue


class WorkSite(metaclass=ABCMeta):
    def __init__(self, dispatcher: Dispatcher, *queue_names: list[Optional[str]]):
        self.dispatcher = dispatcher
        self.queues = [
            dispatcher.queues[queue_name]
            for queue_name in queue_names
            if self.test_queue(queue_name, dispatcher.queues[queue_name])
        ]
        self.stop = False

    @abstractmethod
    def test_queue(self, name: str, queue: WorkQueue) -> bool:
        raise NotImplementedError


class LocalMemoryWorkSite(WorkSite):
    """A work site capable of acquiring tasks from ``LocalMemoryWorkQueue`` and similar.

    Cannot ``dispatch_forever`` because that's not really a good idea with local memory.
    """

    def test_queue(self, name: str, queue: WorkQueue) -> bool:
        if not hasattr(queue, "messages"):
            raise ValueError(f"{name} incompatible with {type(self)}")

        return True

    def dispatch_until_exhausted(self):
        """Dispatch from each queue in turn until it runs out of messages,
        then move on."""

        for task_queue in self.queues:
            while task_queue.messages:
                self.dispatcher.dispatch(task_queue.messages.pop())


class RedisWorkSite(WorkSite):
    """A work site capable of acquiring tasks from ``RedisWorkQueue`` and similar."""

    def test_queue(self, name: str, queue: WorkQueue) -> bool:
        if (
            not hasattr(queue, "redis")
            or not hasattr(queue, "queue")
            or not hasattr(queue, "url")
        ):
            raise ValueError(f"{name} incompatible with {type(self)}")

        return True

    def dispatch_until_exhausted(self):
        """Dispatch from each queue in turn until it runs out of messages,
        then move on."""

        for task_queue in self.queues:
            while message := task_queue.redis.lpop(task_queue.queue):
                self.dispatcher.dispatch(message)

    def dispatch_forever(self):
        """Dispatch until asked to stop.

        Will collect queues from identifiably identical redis instances together,
        and do a single ``BLPOP`` to get the next message from all queues
        from an instance.
        Configured queues are permuted before ``BLPOP`` to ensure
        a single very busy queue does not take over.
        """

        by_redis = [
            (redis.Redis.from_url(url), [queue.queue for queue in queues])
            for url, queues in groupby(
                sorted(self.queues, key=lambda q: q.url), key=lambda q: q.url
            )
        ]

        while not self.stop:
            for r, queues in by_redis:
                random.shuffle(queues)
                if message := r.blpop(queues, 1):
                    self.dispatcher.dispatch(message[1])
