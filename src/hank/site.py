"""A site is configured with a dispatcher to perform work from queues."""

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from itertools import groupby
import random
from typing import Optional

import redis

from .dispatcher import Dispatcher
from .work_queue import WorkQueue


class BaseWorkSite(metaclass=ABCMeta):
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
        pass


class LocalMemoryWorkSite(BaseWorkSite):
    def test_queue(self, name: str, queue: WorkQueue) -> bool:
        if not hasattr(queue, "messages"):
            raise ValueError(f"{name} incompatible with {type(self)}")

        return True

    def dispatch_until_exhausted(self):
        for task_queue in self.queues:
            while task_queue.messages:
                self.dispatcher.dispatch(task_queue.messages.pop())


class RedisWorkSite(BaseWorkSite):
    def test_queue(self, name: str, queue: WorkQueue) -> bool:
        if (
            not hasattr(queue, "redis")
            or not hasattr(queue, "queue")
            or not hasattr(queue, "url")
        ):
            raise ValueError(f"{name} incompatible with {type(self)}")

        return True

    def dispatch_until_exhausted(self):
        for task_queue in self.queues:
            while message := task_queue.redis.lpop(task_queue.queue):
                self.dispatcher.dispatch(message)

    def dispatch_forever(self):
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