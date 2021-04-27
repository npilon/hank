"""Result Stores store the results of executing plans according to tasks."""

from typing import Any, Protocol
from uuid import UUID


class ResultStore(Protocol):
    def store(self, task_id: UUID, result: Any):
        pass

    def get(self, task_id: UUID) -> Any:
        pass


class LocalMemoryResultStore:
    def __init__(self):
        self.data = {}

    def store(self, task_id: UUID, result: Any):
        self.data[task_id] = result

    def get(self, task_id: UUID) -> Any:
        return self.data[task_id]


class RedisResultStore:
    def __init__(self, url: str):
        pass

    def store(self, task_id: UUID, result: Any):
        pass

    def get(self, task_id: UUID) -> Any:
        pass
