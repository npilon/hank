"""Plans are decorated Python callables.

Each is a specification of how to do work.
Plans can be used to create tasks,
or can receive tasks from a dispatcher to execute.
"""

from functools import partial
from typing import Callable, Protocol, runtime_checkable

from .task import Task


class Result:
    pass


@runtime_checkable
class Plan(Protocol):
    def task(*args, **kwargs) -> Task:
        pass

    def receive(task: Task):
        pass


def derive_plan_path(fn: Callable) -> str:
    if fn.__module__ != "__main__":
        return f"/{fn.__module__}.{fn.__name__}".replace(".", "/")
    else:
        return f"/{fn.__name__}"


def plan(fn: Callable) -> Callable:
    fn.task = partial(Task, plan=derive_plan_path(fn))
    fn.receive = fn

    return fn


def argument_unpacking_task(*args, plan: Callable, **kwargs):
    return Task(plan=plan, params={"args": args, "kwargs": kwargs})


def argument_unpacking_receive(task: Task, *, plan: Callable):
    task.worker.store_result(plan(*task.params["args"], **task.params["kwargs"]))


def argument_unpacking_plan(fn: Callable) -> Callable:
    fn.task = partial(argument_unpacking_task, plan=derive_plan_path(fn))
    fn.receive = partial(argument_unpacking_receive, plan=fn)

    return fn
