"""Dispatchers handle the mechanisms of submitting and accepting tasks."""

from .plan import Plan
from .result_store import ResultStore
from .task import Task
from .work_queue import WorkQueue


class Dispatcher:
    def send(self, task: Task):
        pass

    def dispatch_forever(self):
        pass

    def dispatch_until_exhausted(self):
        pass

    def add_result_store(self, default: ResultStore = None, **kwargs):
        pass

    def add_queue(self, default: WorkQueue = None, **kwargs):
        pass

    def add_plan(self, plan: Plan):
        pass
