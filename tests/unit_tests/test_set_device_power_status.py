import pytest
from APsystemsEZ1 import Status


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_status, expected_status, test_id",
    [
        ("0", Status.normal, "happy_path_start_inverter_with_0"),
        ("ON", Status.normal, "happy_path_start_inverter_with_ON"),
        ("1", Status.alarm, "happy_path_stop_inverter_with_1"),
        ("SLEEP", Status.alarm, "happy_path_stop_inverter_with_SLEEP"),
        ("OFF", Status.alarm, "happy_path_stop_inverter_with_OFF"),
    ],
)
async def test_set_device_power_status_happy_paths(
    input_status, expected_status, test_id, mock_response
):
    # Arrange
    ez1m = mock_response({"data": {"status": expected_status.value}, "status": 0})

    # Act
    result = await ez1m.set_device_power_status(input_status)

    # Assert
    assert result == expected_status, f"Test Failed: {test_id}"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_status, test_id",
    [
        ("", "error_case_empty_string"),
        ("2", "error_case_invalid_number"),
        ("ONN", "error_case_typo_in_on"),
        ("SLEEEP", "error_case_typo_in_sleep"),
        ("OFFFF", "error_case_typo_in_off"),
        (None, "error_case_none_value"),
        (3, "error_case_numeric_out_of_range"),
        (True, "error_case_boolean_true"),
        (False, "error_case_boolean_false"),
    ],
)
async def test_set_device_power_status_error_cases(
    input_status, test_id, mock_response
):
    # Arrange
    ez1m = mock_response(None)

    # Assert
    with pytest.raises(ValueError) as exc_info:
        await ez1m.set_device_power_status(input_status)
    assert "Invalid power status" in str(exc_info.value), f"Test Failed: {test_id}"
