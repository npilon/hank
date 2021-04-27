"""Work queues can submit and listen for tasks."""

from collections.abc import Generator
from typing import Protocol

from .task import Task


class WorkQueue(Protocol):
    def send(self, task: Task):
        pass

    def receive(self) -> Generator[Task]:
        pass


class LocalMemoryWorkQueue:
    def __init__(self):
        self.queue = []

    def send(self, task: Task):
        self.queue.append(task)

    def receive(self) -> Generator[Task]:
        while self.queue:
            yield self.queue.pop()


class RedisWorkQueue:
    def __init__(self, url: str):
        pass

    def send(self, task: Task):
        pass

    def receive(self) -> Generator[Task]:
        pass
