"""Dispatchers handle the mechanisms of submitting and accepting tasks."""

import dataclasses
import json
import uuid

from .plan import derive_plan_path, Plan
from .result_store import ResultStore
from .task import Task, Worker
from .work_queue import WorkQueue


class Dispatcher:
    def __init__(self):
        self.plans = {}
        self.queues = {}
        self.result_stores = {}

    def send(self, task: Task):
        task_id = uuid.uuid4()
        message = json.dumps(
            {
                "task_id": str(task_id),
                "task": dataclasses.asdict(task),
            }
        ).encode("utf8")
        self.queues[task.queue].send(message)
        return task_id

    def dispatch(self, message):
        message = json.loads(message)
        task = Task(**message["task"])
        task.worker = Worker(
            task_id=message["task_id"],
            result_store=(
                self.result_stores[
                    task.store_result if task.store_result is not True else None
                ]
                if task.store_result is not False
                else None
            ),
        )
        self.plans[message["plan"]].receive(task)

    def dispatch_forever(self):
        pass

    def dispatch_until_exhausted(self):
        pass

    def add_result_store(self, default: ResultStore = None, **kwargs):
        if default:
            kwargs[None] = default

        self.result_stores.update(kwargs)

    def add_queue(self, default: WorkQueue = None, **kwargs):
        if default:
            kwargs[None] = default

        self.queues.update(kwargs)

    def add_plan(self, plan: Plan):
        self.plans[derive_plan_path(plan)] = plan
