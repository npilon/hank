"""Tasks are specifications of jobs to be done."""

from __future__ import annotations

import copy
import dataclasses
from typing import Any, Union
import uuid

from .result_store import ResultStore


class Worker:
    def __init__(self, task_id: uuid.UUID, result_store: ResultStore):
        self.task_id = task_id
        self.result_store = result_store

    def store_result(self, result):
        if self.result_store:
            self.result_store.store(self.task_id, result)


@dataclasses.dataclass
class Task:
    """Provide a description of work to be done that can easily be serialized
    to/from JSON."""

    #: Name of a registered plan.
    plan: str
    #: Params to be provided to the plan during dispatch.
    params: dict[str, Any]
    #: The queue to submit this task to.
    queue: str = None
    #: The result store to store this task's results in.
    #:
    #: * True or None - default result store
    #: * False - no result store
    #: * string - named result store
    store_result: Union[bool, str, None] = False
    #: The worker executing this task.
    worker: Worker = None

    def options(self, **kwargs):
        return Task(
            plan=self.plan,
            params=copy.copy(self.params),
            queue=(kwargs["queue"] if "queue" in kwargs else self.queue),
            store_result=(
                kwargs["store_result"]
                if "store_result" in kwargs
                else self.store_result
            ),
        )
