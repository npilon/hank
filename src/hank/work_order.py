import dataclasses
from typing import Any, Dict


@dataclasses.dataclass
class WorkOrder:
    """Work Orders are specifications of jobs to be done.
    """

    #: Name of a registered job.
    job: str
    #: Params to be provided to the job during dispatch.
    params: Dict[str, Any]
    #: The dispatcher executing this work order.
    dispatcher: Any = None
