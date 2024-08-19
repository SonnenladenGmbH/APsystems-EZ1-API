import pytest

from APsystemsEZ1 import InverterReturnedError


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_id, output_data, expected_status",
    [
        ("happy-on", {"data": {"status": 0}, "status": 0}, True),
        ("happy-off", {"data": {"status": 1}, "status": 0}, False),
    ],
)
async def test_get_device_power_status_happy_paths(
    test_id, output_data, expected_status, mock_response
):
    # Arrange
    ez1m = mock_response(output_data)

    # Act
    status = await ez1m.get_device_power_status()

    # Assert
    assert status == expected_status, f"Test failed for {test_id}"

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_id, output_data",
    [
        ("edge-no-status", {"data": {"status": ""}, "status": 0}),
    ],
)
async def test_get_device_power_status_value_error(test_id, output_data, mock_response):
    # Arrange
    ez1m = mock_response(output_data)

    # Assert
    with pytest.raises(InverterReturnedError):
        await ez1m.get_device_power_status()

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_id, output_data",
    [
        ("edge-empty-data", {"data": {}, "status": 0}),
        ("error-malformed-data", {"wrong": "data"}),
    ],
)
async def test_get_device_power_status_key_error(test_id, output_data, mock_response):
    # Arrange
    ez1m = mock_response(output_data)

    # Assert
    with pytest.raises(KeyError) as exc_info:
        await ez1m.get_device_power_status()
