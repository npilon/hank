import dataclasses
from typing import Any, Dict


@dataclasses.dataclass
class Task:
    """Tasks are specifications of jobs to be done."""

    #: Name of a registered plan.
    plan: str
    #: Params to be provided to the plan during dispatch.
    params: Dict[str, Any]
    #: The queue to submit this task to.
    queue: str = None
    #: The result store to store this task's results in.
    store_result: str = None
    #: The dispatcher executing this task.
    dispatcher: Any = None
