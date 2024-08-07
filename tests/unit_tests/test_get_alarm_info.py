import pytest
from APsystemsEZ1 import ReturnAlarmInfo


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "response_data, expected_result, test_id",
    [
        # Happy path tests with various realistic test values
        (
            {"og": "0", "isce1": "0", "isce2": "0", "oe": "0"},
            ReturnAlarmInfo(
                offgrid=False,
                shortcircuit_1=False,
                shortcircuit_2=False,
                operating=True,
            ),
            "happy_path_all_normal",
        ),
        (
            {"og": "1", "isce1": "0", "isce2": "0", "oe": "0"},
            ReturnAlarmInfo(
                offgrid=True,
                shortcircuit_1=False,
                shortcircuit_2=False,
                operating=True,
            ),
            "happy_path_off_grid_alarm",
        ),
        # Edge cases
        (
            {"og": "0", "isce1": "1", "isce2": "1", "oe": "1"},
            ReturnAlarmInfo(
                offgrid=False,
                shortcircuit_1=True,
                shortcircuit_2=True,
                operating=False,
            ),
            "edge_case_multiple_alarms",
        ),
    ],
)
async def test_get_alarm_info_happy_paths(
    response_data, expected_result, test_id, mock_response
):
    # Arrange
    ez1m = mock_response({"data": response_data, "status": 0})

    # Act
    result = await ez1m.get_alarm_info()

    # Assert
    assert result == expected_result, f"Test failed for {test_id}"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "expected_result, test_id",
    [
        # Error cases
        (None, "error_case_none_response"),
    ],
)
async def test_get_alarm_info_none_response(expected_result, test_id, mock_response):
    # Arrange
    ez1m = mock_response(None)

    # Act
    result = await ez1m.get_alarm_info()

    # Assert
    assert result is expected_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "response_data, test_id",
    [
        # Error cases
        ({}, "error_case_empty_response"),
    ],
)
async def test_get_alarm_info_empty_response(response_data, test_id, mock_response):
    # Arrange
    ez1m = mock_response({"data": response_data, "status": 0})

    # Assert
    with pytest.raises(KeyError) as exc_info:
        await ez1m.get_alarm_info()
    assert "og" in str(exc_info.value), f"Test Failed: {test_id}"
