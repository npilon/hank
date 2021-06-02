from unittest import mock

import pytest

from hank.dispatcher import DispatchedTask, DispatchedTaskTimeout


def test_timeout():
    with pytest.raises(DispatchedTaskTimeout):
        dt = DispatchedTask(
            result_store=mock.Mock(get=mock.Mock(side_effect=KeyError())), task_id=None
        )
        dt.wait(timeout=0.5)

    assert len(dt.result_store.get.mock_calls) == 3
