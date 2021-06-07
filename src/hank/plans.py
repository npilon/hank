"""Plans are decorated Python callables.

Each is a specification of how to do work.
Plans can be used to create tasks,
or can receive tasks from a dispatcher to execute.
"""

from __future__ import annotations

from typing import Any, Callable, Protocol, runtime_checkable, Union

from .task import Task


@runtime_checkable
class Plan(Protocol):
    plan_path: str

    def task(*args, **kwargs) -> Task:
        raise NotImplementedError

    def receive(task: Task):
        raise NotImplementedError


def _derive_plan_path(fn: Callable) -> str:
    if fn.__module__ != "__main__":
        return f"/{fn.__module__}.{fn.__name__}".replace(".", "/")
    else:
        return f"/{fn.__name__}"


def plan(fn: Callable) -> Callable:
    """A basic plan. Expects to receive a ``Task`` as an argument."""

    def _plan(
        params: dict[str, Any],
        queue: str = None,
        store_result: Union[bool, str, None] = False,
    ):
        return Task(
            plan=fn.plan_path, params=params, queue=queue, store_result=store_result
        )

    fn.task = _plan
    fn.receive = fn
    fn.plan_path = _derive_plan_path(fn)

    return fn


def argument_unpacking_plan(fn: Callable) -> Callable:
    """A plan that follows python conventions around argument passing
    and returning results."""

    def argument_unpacking_task(*args, **kwargs):
        return Task(plan=fn.plan_path, params={"args": args, "kwargs": kwargs})

    def argument_unpacking_receive(task: Task):
        task.worker.store_result(fn(*task.params["args"], **task.params["kwargs"]))

    fn.task = argument_unpacking_task
    fn.receive = argument_unpacking_receive
    fn.plan_path = _derive_plan_path(fn)

    return fn
