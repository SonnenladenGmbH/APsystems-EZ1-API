import APsystemsEZ1
import datetime
import pytest


class MyDateTime(datetime.datetime):
    _custom_now = None

    class datetime:
        @classmethod
        def set_custom_now(cls, custom_now) -> None:
            cls._custom_now = custom_now

        @classmethod
        def now(cls):
            if cls._custom_now is not None:
                return cls._custom_now
            raise ValueError


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("state_data, days, expected_state, test_step_id"),
    [
        (
            [0.0, 1.0, 2.1, 3.1],
            [1, 1, 1, 1],
            [0.0, 1.0, 2.1, 3.1],
            "normal count up",
        ),
        (
            [0.0, 1.0, 2.1, 3.1, None, 1.1, 3.14],
            [1, 1, 1, 1, 1, 2, 2],
            [0.0, 1.0, 2.1, 3.1, None, 1.1, 3.14],
            "normal count up, unavailable, day change",
        ),
        (
            [0.0, 1.0, 2.1, 3.1, 0.0, 1.1, 3.14],
            [1, 1, 1, 1, 1, 2, 2],
            [0.0, 1.0, 2.1, 3.1, 3.1, 1.1, 3.14],
            "normal count up, reset zero, day change",
        ),
        (
            [2.1, 3.2, 0.0, 1.2, 2.2],
            [1, 1, 1, 1, 1],
            [2.1, 3.2, 3.2, 4.4, 5.4],
            "fall back to zero (restart) during same day",
        ),
        (
            [2.1, 3.2, 1.0, 1.2, 2.2],
            [1, 1, 1, 1, 1],
            [2.1, 3.2, 4.2, 4.4, 5.4],
            "fall back to 1.0 (restart) during same day",
        ),
        (
            [2.1, 3.2, 3.4, 3.5, 3.6],
            [1, 1, 1, 2, 2],
            [2.1, 3.2, 3.4, 3.5, 3.6],
            "continous production with day change",
        ),
        (
            [2.1, 3.1, None, 0.0, 4.2, 5.2],
            [1, 1, 1, 2, 2, 2],
            [2.1, 3.1, None, 0.0, 4.2, 5.2],
            "next day starts higher than previous ended",
        ),
    ],
)
async def test_debounce(monkeypatch, state_data, days, expected_state, test_step_id):

    assert len(state_data) == len(days) and len(state_data) == len(
        expected_state
    ), "'state_data', 'days', 'expected_state' need to have equal length."

    ez1m = APsystemsEZ1.APsystemsEZ1M(ip_address="0.0.0.0", enable_debounce=True)
    debounce_state = (
        APsystemsEZ1.APsystemsEZ1M._DebounceVal(  # pylint: disable=protected-access
            0.0, 0.0
        )
    )

    for value in list(zip(state_data, days, expected_state)):
        MyDateTime.datetime.set_custom_now(MyDateTime(2024, 8, value[1]))
        # Patch (manipulate time)
        monkeypatch.setattr(APsystemsEZ1, "datetime", MyDateTime)
        # Act
        result_state = ez1m._debounce(  # pylint: disable=protected-access
            debounce_state, value[0]
        )
        # Assert
        assert (
            result_state == value[2]
        ), f"Test failed for {test_step_id}, sample {value=}"
