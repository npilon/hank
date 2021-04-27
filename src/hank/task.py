"""Tasks are specifications of jobs to be done."""

import copy
import dataclasses
from typing import Any, Dict, Union


@dataclasses.dataclass
class Task:
    """The most basic, fundamental style of task."""

    #: Name of a registered plan.
    plan: str
    #: Params to be provided to the plan during dispatch.
    params: Dict[str, Any]
    #: The queue to submit this task to.
    queue: str = None
    #: The result store to store this task's results in.
    #:
    #: * True or None - default result store
    #: * False - no result store
    #: * string - named result store
    store_result: Union[bool, str, None] = False
    #: The dispatcher executing this task.
    dispatcher: Any = None

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
