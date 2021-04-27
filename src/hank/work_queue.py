"""Work queues can submit and listen for tasks."""

from __future__ import annotations

from collections.abc import Generator
from typing import Protocol


class WorkQueue(Protocol):
    def send(self, message: bytes):
        pass

    def receive(self) -> Generator[bytes]:
        pass


class LocalMemoryWorkQueue:
    def __init__(self):
        self.queue = []

    def send(self, message: bytes):
        self.queue.append(message)

    def receive(self) -> Generator[bytes]:
        while self.queue:
            yield self.queue.pop()


class RedisWorkQueue:
    def __init__(self, url: str):
        pass

    def send(self, message: bytes):
        pass

    def receive(self) -> Generator[bytes]:
        pass
