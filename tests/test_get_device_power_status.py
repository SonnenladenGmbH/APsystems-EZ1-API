import pytest
import APsystemsEZ1
from APsystemsEZ1 import Status
from unittest.mock import AsyncMock


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_id, mock_response, expected_status",
    [
        # Happy path tests
        ("happy-on", {"data": {"status": "0"}}, Status.normal),
        ("happy-off", {"data": {"status": "1"}}, Status.alarm),
        # Edge cases
        ("edge-empty-data", {"data": {}}, None),
        ("edge-no-status", {"data": {"status": ""}}, None),
        # Error cases
        ("error-null-response", None, None),
        ("error-malformed-data", {"wrong": "data"}, None),
    ],
)
async def test_get_device_power_status(test_id, mock_response, expected_status):
    # Arrange
    apsystem = APsystemsEZ1.APsystemsEZ1M(ip_address="0.0.0.0")
    apsystem._request = AsyncMock(return_value=mock_response)

    # Act
    status = await apsystem.get_device_power_status()

    # Assert
    assert status == expected_status, f"Test failed for {test_id}"
