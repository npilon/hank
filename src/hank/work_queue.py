"""Work queues can submit and listen for tasks."""

from __future__ import annotations

from typing import Protocol

import redis


class WorkQueue(Protocol):
    def send(self, message: bytes):
        pass

    def poll(self, timeout: int) -> bytes:
        pass


class LocalMemoryWorkQueue:
    def __init__(self):
        self.queue = []

    def send(self, message: bytes):
        self.queue.append(message)

    def poll(self, timeout: int) -> bytes:
        if self.queue:
            return self.queue.pop()


class RedisWorkQueue:
    def __init__(self, url: str, queue: str):
        self.queue = queue
        self.redis = redis.Redis.from_url(url)

    def send(self, message: bytes):
        self.redis.rpush(self.queue, message)

    def poll(self, timeout: int) -> bytes:
        maybe_message = self.redis.blpop(self.queue, timeout)
        if maybe_message:
            return maybe_message[1]
