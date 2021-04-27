"""Plans are decorated Python callables.

Each is a specification of how to do work.
Plans can be used to create tasks,
or can receive tasks from a dispatcher to execute.
"""

from functools import partial
from typing import Callable, Protocol, runtime_checkable

from .task import Task


@runtime_checkable
class Plan(Protocol):
    def task():
        pass


def derive_plan_path(fn: Callable) -> str:
    if fn.__module__ != "__main__":
        return f"/{fn.__module__}.{fn.__name__}".replace(".", "/")
    else:
        return f"/{fn.__name__}"


def plan(fn: Callable) -> Callable:
    fn.task = partial(Task, plan=derive_plan_path(fn))
    return fn
