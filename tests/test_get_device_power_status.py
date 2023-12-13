import pytest
import APsystemsEZ1
from APsystemsEZ1 import Status
from unittest.mock import AsyncMock


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_id, mock_response, expected_status",
    [
        ("happy-on", {"data": {"status": 0}}, Status.normal),
        ("happy-off", {"data": {"status": 1}}, Status.alarm),
    ],
)
async def test_get_device_power_status_happy_paths(
    test_id, mock_response, expected_status
):
    # Arrange
    apsystem = APsystemsEZ1.APsystemsEZ1M(ip_address="0.0.0.0")
    apsystem._request = AsyncMock(return_value=mock_response)

    # Act
    status = await apsystem.get_device_power_status()

    # Assert
    assert status == expected_status, f"Test failed for {test_id}"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_id, mock_response",
    [
        ("edge-no-status", {"data": {"status": ""}}),
    ],
)
async def test_get_device_power_status_value_error(test_id, mock_response):
    # Arrange
    apsystem = APsystemsEZ1.APsystemsEZ1M(ip_address="0.0.0.0")
    apsystem._request = AsyncMock(return_value=mock_response)

    # Assert
    with pytest.raises(ValueError) as exc_info:
        await apsystem.get_device_power_status()
    assert "is not a valid Status" in str(exc_info.value), f"Test Failed: {test_id}"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_id, mock_response",
    [
        ("edge-empty-data", {"data": {}}),
        ("error-malformed-data", {"wrong": "data"}),
    ],
)
async def test_get_device_power_status_key_error(test_id, mock_response):
    # Arrange
    apsystem = APsystemsEZ1.APsystemsEZ1M(ip_address="0.0.0.0")
    apsystem._request = AsyncMock(return_value=mock_response)

    # Assert
    with pytest.raises(KeyError) as exc_info:
        await apsystem.get_device_power_status()
