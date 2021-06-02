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
from hank import argument_unpacking_plan, Dispatcher, LocalMemoryWorkQueue, LocalMemoryResultStore, LocalMemoryWorkSite


# argument_unpacking_plan includes setting result from return value.
@argument_unpacking_plan
def do_arithmetic(x, y):
    return x + y


dispatcher = Dispatcher()


if __name__ == '__main__':
    result_store = LocalMemoryResultStore()
    # Unnamed queue - default for all messages.
    dispatcher.add_queue(default=LocalMemoryWorkQueue())
    # Unnamed result store - default for any results.
    dispatcher.add_result_store(result_store)
    dispatcher.add_plan(do_arithmetic)
    # Store result could also take the name of a configured result store.
    result = dispatcher.send(
        do_arithmetic.task(2, 3).options(store_result=True)
    )
    work_site = LocalMemoryWorkSite(dispatcher, None)
    work_site.dispatch_until_exhausted()
    print(result.wait())
```

```python
import sys

from hank import Dispatcher, plan, RedisWorkQueue, RedisResultStore, RedisWorkSite


@plan
def do_arithmetic(task):
    task.worker.store_result(sum(task.params['args']))


dispatcher = Dispatcher()


if __name__ == '__main__':
    dispatcher.add_queue(example_queue=RedisWorkQueue(url='redis://localhost:6379/0', queue='example_queue'))
    dispatcher.add_result_store(example_store=RedisResultStore('redis://localhost:6379/1'))
    dispatcher.add_plan(do_arithmetic)

    if sys.argv[1] == 'worker':
        work_site = RedisWorkSite(dispatcher, 'example_queue')
        work_site.dispatch_forever()
    else:
        result = dispatcher.send(
            do_arithmetic.task(
                params=dict(args=[int(i) for i in sys.argv[1:]]),
                queue='example_queue',
                store_result='example_store',
            ),
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
