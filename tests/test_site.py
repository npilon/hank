import pytest

from hank.dispatcher import Dispatcher
from hank.work_queue import LocalMemoryWorkQueue, RedisWorkQueue
from hank.site import LocalMemoryWorkSite, RedisWorkSite


@pytest.mark.parametrize(
    "work_site_cls, work_queue_maker",
    [
        (
            LocalMemoryWorkSite,
            lambda: RedisWorkQueue(
                url="redis://localhost:6379/0", queue="example_queue"
            ),
        ),
        (RedisWorkSite, lambda: LocalMemoryWorkQueue()),
    ],
)
def test_mismatched_work_queue(work_site_cls, work_queue_maker):
    d = Dispatcher()
    d.add_queue(default=work_queue_maker())
    with pytest.raises(ValueError):
        work_site_cls(d, None)
