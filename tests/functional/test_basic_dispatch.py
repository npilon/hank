import threading

from hank import (
    plan,
    Dispatcher,
    RedisWorkQueue,
    RedisResultStore,
    RedisWorkSite,
)


@plan
def do_arithmetic(task):
    task.worker.store_result(sum(task.params["args"]))


def test_argument_dispatching():
    dispatcher = Dispatcher()
    dispatcher.add_queue(
        example_queue=RedisWorkQueue(
            url="redis://localhost:6379/0", queue="example_queue"
        )
    )
    dispatcher.add_result_store(
        example_store=RedisResultStore("redis://localhost:6379/1")
    )
    dispatcher.add_plan(do_arithmetic)
    work_site = RedisWorkSite(dispatcher, "example_queue")

    worker = threading.Thread(target=work_site.dispatch_forever)

    try:
        worker.start()
        result = dispatcher.send(
            do_arithmetic.task(
                params=dict(args=[1, 2, 3, 4]),
                queue="example_queue",
                store_result="example_store",
            ),
        )
        assert result.wait(timeout=2) == 10
        work_site.stop = True
    finally:
        worker.join(timeout=1)
        if worker.is_alive():
            raise Exception()
