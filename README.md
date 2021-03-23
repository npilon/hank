# hank

[![Build Status](https://github.com/npilon/hank/workflows/Build%20Main/badge.svg)](https://github.com/npilon/hank/actions)
[![Documentation](https://github.com/npilon/hank/workflows/Documentation/badge.svg)](https://npilon.github.io/hank/)
[![Code Coverage](https://codecov.io/gh/npilon/hank/branch/main/graph/badge.svg)](https://codecov.io/gh/npilon/hank)

Hank is an asynchronous job processing and orchestration system.

---

## Features

- Dispatching of work orders for individual jobs
- Orchestration of work flows of multiple work orders
- Support for managing large batch processes from running jobs

## Quick Start

```python
from hank import Dispatcher, LocalMemoryWorkQueue, LocalMemoryResultStore, task


@task
def arithmetic_task(x, y):
    return x + y


dispatcher = Dispatcher()


if __name__ == '__main__':
    result_store = LocalMemoryResultStore()
    dispatcher.add_queue(LocalMemoryWorkQueue())
    dispatcher.add_result_store(result_store)
    dispatcher.add_job(arithmetic_task)
    result = dispatcher.send(arithmetic_task.work_order(2, 3))
    dispatcher.dispatch_until_exhausted()
    print(result.wait())
```

```python
import sys

from hank import Dispatcher, job, RedisWorkQueue, RedisResultStore


@job
def arithmetic_job(work_order):
    work_order.dispatcher.store_result(sum(work_order.params['args']))


dispatcher = Dispatcher()


if __name__ == '__main__':
    result_store = RedisResultStore('redis://localhost:6379/1')
    dispatcher.add_queue(RedisWorkQueue('redis://localhost:6379/0'))
    dispatcher.add_result_store(result_store)
    dispatcher.add_job(arithmetic_job)

    if sys.argv[1] == 'worker':
        dispatcher.dispatch_forver()
    else:
        result = dispatcher.send(
            arithmetic_job.work_order(
                args=[int(i) for i in sys.argv[1:]]
            )
        )
        print(result.wait())
```


## Installation

**Stable Release:** `pip install hank`<br>
**Development Head:** `pip install git+https://github.com/npilon/hank.git`

## Documentation

For full package documentation please visit [npilon.github.io/hank](https://npilon.github.io/hank).

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for information related to developing the code.

## The Four Commands You Need To Know

1. `pip install -e .[dev]`

    This will install your package in editable mode with all the required development
    dependencies (i.e. `tox`).

2. `make build`

    This will run `tox` which will run all your tests in both Python 3.7
    and Python 3.8 as well as linting your code.

3. `make clean`

    This will clean up various Python and build generated files so that you can ensure
    that you are working in a clean environment.

4. `make docs`

    This will generate and launch a web browser to view the most up-to-date
    documentation for your Python package.

**Apache Software License 2.0**
