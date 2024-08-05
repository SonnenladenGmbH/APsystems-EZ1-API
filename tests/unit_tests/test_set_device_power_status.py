import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_status, expected_status, test_id",
    [
        (True, 0, "happy_path_start_inverter_with_tue"),
        (False, 1, "happy_path_start_inverter_with_False"),
    ],
)
async def test_set_device_power_status_happy_paths(
    input_status, expected_status, test_id, mock_response
):
    # Arrange
    ez1m = mock_response({"data": {"status": expected_status}, "status": 0})

    # Act
    result = await ez1m.set_device_power_status(input_status)

    # Assert
    assert result == input_status, f"Test Failed: {test_id}"


