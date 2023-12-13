import pytest
from APsystemsEZ1 import ReturnAlarmInfo, Status


# Replace 'ReturnAlarmInfo' with the actual type if it's not the correct one
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "response_data, expected_result, test_id",
    [
        # Happy path tests with various realistic test values
        (
            {"og": "0", "isce1": "0", "isce2": "0", "oe": "0"},
            ReturnAlarmInfo(og=Status.normal, isce1=Status.normal, isce2=Status.normal, oe=Status.normal),
            "happy_path_all_normal",
        ),
        (
            {"og": "1", "isce1": "0", "isce2": "0", "oe": "0"},
            ReturnAlarmInfo(og=Status.alarm, isce1=Status.normal, isce2=Status.normal, oe=Status.normal),
            "happy_path_off_grid_alarm",
        ),
        # Edge cases
        (
            {"og": "0", "isce1": "1", "isce2": "1", "oe": "1"},
            ReturnAlarmInfo(og=Status.normal, isce1=Status.alarm, isce2=Status.alarm, oe=Status.alarm),
            "edge_case_multiple_alarms",
        ),
        # Error cases
        ({}, None, "error_case_empty_response"),
        (None, None, "error_case_none_response"),
    ],
)
async def test_get_alarm_info(response_data, expected_result, test_id, mock_response):
    # Arrange
    ez1m = mock_response({"data": response_data})

    # Act
    result = await ez1m.get_alarm_info()

    # Assert
    assert result == expected_result, f"Test failed for {test_id}"
