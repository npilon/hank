"""Result Stores store the results of executing plans according to tasks."""

import json
from typing import Any, Protocol
from uuid import UUID

import redis


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
        self.redis = redis.Redis.from_url(url)

    def store(self, task_id: UUID, result: Any):
        self.redis.set(str(task_id), json.dumps(result))

    def get(self, task_id: UUID) -> Any:
        r = self.redis.get(str(task_id))
        if r is None:
            raise KeyError()
        self.redis.delete(str(task_id))
        return json.loads(r)
