# -*- coding: utf-8 -*-

"""Top-level package for hank."""

from .dispatcher import Dispatcher
from .plan import argument_unpacking_plan
from .result_store import LocalMemoryResultStore
from .work_queue import LocalMemoryWorkQueue

__author__ = "Nicholas Owen Paul Pilon"
__email__ = "npilon@gmail.com"
# Do not edit this string manually, always use bumpversion
# Details in CONTRIBUTING.md
__version__ = "0.0.0"


__all__ = [
    "argument_unpacking_plan",
    "Dispatcher",
    "LocalMemoryResultStore",
    "LocalMemoryWorkQueue",
]


def get_module_version():
    return __version__
