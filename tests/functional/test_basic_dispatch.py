import subprocess
import sys

from hank import (
    plan,
    Dispatcher,
    RedisWorkQueue,
    RedisResultStore,
)


@plan
def do_arithmetic(task):
    task.worker.store_result(sum(task.params["args"]))


def configure(dispatcher):
    dispatcher.add_queue(
        example_queue=RedisWorkQueue(
            url="redis://localhost:6379/0", queue="example_queue"
        )
    )
    dispatcher.add_result_store(
        example_store=RedisResultStore("redis://localhost:6379/1")
    )
    do_arithmetic.__module__ = 'tests.functional.test_basic_dispatch'
    dispatcher.add_plan(do_arithmetic)


def worker():
    dispatcher = Dispatcher()
    configure(dispatcher)
    dispatcher.dispatch_forever()


def test_argument_dispatching():
    worker = subprocess.Popen(
        [sys.executable, __file__, "worker"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    dispatcher = Dispatcher()
    configure(dispatcher)


    try:
        result = dispatcher.send(
            do_arithmetic.task(
                params=dict(args=[1, 2, 3, 4]),
                queue="example_queue",
                store_result="example_store",
            ),
        )
        assert result.wait(timeout=2) == 10
    finally:
        worker.terminate()
        print(worker.stdout.read())
        print(worker.stderr.read())


if __name__ == "__main__":
    if sys.argv[1] == "worker":
        worker()
