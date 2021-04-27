"""Dispatchers handle the mechanisms of submitting and accepting tasks."""

import dataclasses
import json
import uuid

from .plan import derive_plan_path, Plan
from .result_store import ResultStore
from .task import Task
from .work_queue import WorkQueue


class Dispatcher:
    def __init__(self):
        self.plans = {}
        self.queues = {}
        self.result_stores = {}

    def send(self, task: Task):
        task_id = uuid.uuid4()
        message = json.dumps(
            {"task_id": task_id, "task": dataclasses.asdict(task)}
        ).encode("utf8")
        self.queues[task.queue].send(message)
        return task_id

    def dispatch(self, message):
        message = json.loads(message)
        task = Task(**message["task"])
        task.dispatcher = self
        result = self.plans[task.plan](task)
        self.result_stores[task.store_result].store(uuid.UUID(task["task_id"]), result)

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
