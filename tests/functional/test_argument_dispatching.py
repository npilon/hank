from hank import (
    argument_unpacking_plan,
    Dispatcher,
    LocalMemoryWorkQueue,
    LocalMemoryResultStore,
    LocalMemoryWorkSite,
)

# argument_unpacking_plan includes setting result from return value.
@argument_unpacking_plan
def do_arithmetic(x, y):
    return x + y


def test_argument_dispatching():
    dispatcher = Dispatcher()

    result_store = LocalMemoryResultStore()
    # Unnamed queue - default for all messages.
    dispatcher.add_queue(LocalMemoryWorkQueue())
    # Unnamed result store - default for any results.
    dispatcher.add_result_store(result_store)
    dispatcher.add_plan(do_arithmetic)
    # Store result could also take the name of a configured result store.
    result = dispatcher.send(do_arithmetic.task(2, 3).options(store_result=True))
    work_site = LocalMemoryWorkSite(dispatcher, None)
    work_site.dispatch_until_exhausted()
    assert result.wait() == 5
