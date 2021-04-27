"""Work queues can submit and listen for tasks."""

from typing import Protocol


class WorkQueue(Protocol):
    pass


class LocalMemoryWorkQueue:
    pass


class RedisWorkQueue:
    def __init__(self, url: str):
        pass
