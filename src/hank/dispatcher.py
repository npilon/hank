"""Dispatchers handle the mechanisms of submitting and accepting tasks."""

import dataclasses
import json
import uuid

from .plans import derive_plan_path, Plan
from .result_store import ResultStore
from .task import Task, Worker
from .work_queue import WorkQueue


class DispatchedTask:
    def __init__(self, result_store: ResultStore, task_id: uuid.UUID):
        self.result_store = result_store
        self.task_id = task_id

    def wait(self):
        while True:
            try:
                return self.result_store.get(self.task_id)
            except KeyError:
                pass


class Dispatcher:
    def __init__(self):
        self.plans = {}
        self.queues = {}
        self.result_stores = {}

    def send(self, task: Task) -> DispatchedTask:
        task_id = uuid.uuid4()
        message = json.dumps(
            {
                "task_id": str(task_id),
                "task": dataclasses.asdict(task),
            }
        ).encode("utf8")
        self.queues[task.queue].send(message)
        if task.store_result is not False:
            return DispatchedTask(
                result_store=self.result_store_for(task), task_id=task_id
            )

    def dispatch(self, message: bytes):
        message = json.loads(message.decode("utf8"))
        task = Task(**message["task"])
        task.worker = Worker(
            task_id=uuid.UUID(message["task_id"]),
            result_store=(
                self.result_store_for(task=task)
                if task.store_result is not False
                else None
            ),
        )
        self.plans[task.plan].receive(task)

    def dispatch_forever(self):
        pass

    def dispatch_until_exhausted(self):
        for task_queue in self.queues.values():
            for message in task_queue.receive():
                self.dispatch(message)

    def add_result_store(self, default: ResultStore = None, **kwargs):
        if default:
            kwargs[None] = default

        self.result_stores.update(kwargs)

    def result_store_for(self, task: Task):
        return self.result_stores[
            task.store_result if task.store_result is not True else None
        ]

    def add_queue(self, default: WorkQueue = None, **kwargs):
        if default:
            kwargs[None] = default

        self.queues.update(kwargs)

    def add_plan(self, plan: Plan):
        self.plans[derive_plan_path(plan)] = plan
