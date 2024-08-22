import APsystemsEZ1
import datetime
from unittest import mock
import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "state_data, days, expected_state, test_step_id",
    [
        (
            [0.0, 1.0, 2.1, 3.1],
            [1, 1, 1, 1],
            3.1,
            "normal count up",
        ),
        (
            [0.0, 1.0, 2.1, 3.1, None, 1.1, 3.14],
            [1, 1, 1, 1, 1, 2, 2],
            3.14,
            "normal count up, unavailable, day change",
        ),
        (
            [0.0, 1.0, 2.1, 3.1, 0.0, 1.1, 3.14],
            [1, 1, 1, 1, 1, 2, 2],
            3.14,
            "normal count up, reset zero, day change",
        ),
        (
            [2.1, 3.2, 0.0, 1.2, 2.2],
            [1, 1, 1, 1, 1],
            5.4,
            "fall back to zero (restart) during same day"
        ),
        (
            [2.1, 3.2, 1.0, 1.2, 2.2],
            [1, 1, 1, 1, 1],
            5.4,
            "fall back to 1.0 (restart) during same day"
        ),
        (
            [2.1, 3.2, 3.4, 3.5, 3.6],
            [1, 1, 1, 2, 2],
            3.6,
            "continous production with day change"
        )
    ],
)

async def test_debounce(
    state_data, days, expected_state, test_step_id):

    assert len(state_data) == len(days), "'state_data' and 'days' need to have equal length."

    ez1m = APsystemsEZ1.APsystemsEZ1M(ip_address="0.0.0.0", enable_debounce=True)
    debounce_state = APsystemsEZ1.APsystemsEZ1M._DebounceVal(0.0, 0.0)
    result_state = None

    with mock.patch('datetime.datetime', wraps=datetime.datetime) as dt:
        for value in list(zip(state_data, days)):
            # Act
            dt.now.return_value = datetime.datetime(2024, 8, value[1])
            result_state = ez1m._debounce(debounce_state, value[0])

    # Assert
    assert result_state == expected_state, f"Test failed for {test_step_id}"
