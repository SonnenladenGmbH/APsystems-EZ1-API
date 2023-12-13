import pytest
import APsystemsEZ1
from unittest.mock import AsyncMock


# Test cases for the happy path with various realistic test values
@pytest.mark.parametrize(
    "test_id, max_power, expected",
    [
        ("happy-100", {"data": {"maxPower": "100"}}, 100),
        ("happy-200", {"data": {"maxPower": "200"}}, 200),
        ("happy-500", {"data": {"maxPower": "500"}}, 500),
    ],
)
@pytest.mark.asyncio
async def test_get_max_power_happy_path(test_id, max_power, expected):
    # Arrange
    apsystem = APsystemsEZ1.APsystemsEZ1M(ip_address="0.0.0.0")
    apsystem._request = AsyncMock(return_value=max_power)

    # Act
    result = await apsystem.get_max_power()

    # Assert
    assert result == expected, f"Test ID: {test_id}"


# Test cases for edge cases
@pytest.mark.parametrize(
    "test_id, max_power, expected",
    [
        ("edge-zero", {"data": {"maxPower": "0"}}, 0),
        ("edge-empty", {"data": {"maxPower": ""}}, None),
        ("edge-none", None, None),
    ],
)
@pytest.mark.asyncio
async def test_get_max_power_edge_cases(test_id, max_power, expected):
    # Arrange
    apsystem = APsystemsEZ1.APsystemsEZ1M(ip_address="0.0.0.0")
    apsystem._request = AsyncMock(return_value=max_power)

    # Act
    result = await apsystem.get_max_power()

    # Assert
    assert result == expected, f"Test ID: {test_id}"
