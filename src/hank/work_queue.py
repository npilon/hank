"""Work queues can submit tasks and be used by work sites to listen for tasks."""

from __future__ import annotations

from typing import Protocol

import redis


class WorkQueue(Protocol):
    def send(self, message: bytes):
        pass


class LocalMemoryWorkQueue:
    """A work queue that keeps a set of tasks in local memory.

    Principally useful for testing or small toy applications.
    """

    def __init__(self):
        self.messages = []

    def send(self, message: bytes):
        self.messages.append(message)


class RedisWorkQueue:
    """A work queue using redis lists.

    The configured queue name will be used as the name of the list.
    """

    def __init__(self, url: str, queue: str):
        self.queue = queue
        self.url = url
        self.redis = redis.Redis.from_url(url)

    def send(self, message: bytes):
        self.redis.rpush(self.queue, message)
