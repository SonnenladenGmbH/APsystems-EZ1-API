import pytest
from unittest.mock import AsyncMock, patch
from APsystemsEZ1 import APsystemsEZ1M, ReturnDeviceInfo, ReturnAlarmInfo, ReturnOutputData, Status

# Constants for use in tests
BASE_URL = "http://192.168.1.100:8050"
VALID_IP = "192.168.1.100"
VALID_PORT = 8050
VALID_TIMEOUT = 10
INVALID_IP = "192.168.1.300"

# Test data for ReturnDeviceInfo
DEVICE_INFO_DATA = {
    "deviceId": "1234567890",
    "devVer": "1.0",
    "ssid": "HomeNetwork",
    "ipAddr": VALID_IP,
    "minPower": 30,
    "maxPower": 800
}

# Test data for ReturnAlarmInfo
ALARM_INFO_DATA = {
    "og": Status.normal,
    "isce1": Status.alarm,
    "isce2": Status.normal,
    "oe": Status.alarm
}

# Test data for ReturnOutputData
OUTPUT_DATA = {
    "p1": 100.0,
    "e1": 50.0,
    "te1": 500.0,
    "p2": 200.0,
    "e2": 100.0,
    "te2": 1000.0
}

# Test data for power status
POWER_STATUS_ON = "0"
POWER_STATUS_OFF = "1"

# Test data for set max power
VALID_MAX_POWER = 500
INVALID_MAX_POWER = 900

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "endpoint, return_value, expected_result, test_id",
    [
        # Happy path tests
        ("getDeviceInfo", {"data": DEVICE_INFO_DATA}, ReturnDeviceInfo(**DEVICE_INFO_DATA), "H1"),
        ("getAlarm", {"data": ALARM_INFO_DATA}, ReturnAlarmInfo(**ALARM_INFO_DATA), "H2"),
        ("getOutputData", {"data": OUTPUT_DATA}, ReturnOutputData(**OUTPUT_DATA), "H3"),
        ("getMaxPower", {"data": {"maxPower": VALID_MAX_POWER}}, VALID_MAX_POWER, "H4"),
        ("setOnOff", {"data": {"status": POWER_STATUS_ON}}, Status.normal, "H5"),
        ("setOnOff", {"data": {"status": POWER_STATUS_OFF}}, Status.alarm, "H6"),
        ("setMaxPower", {"data": {"maxPower": VALID_MAX_POWER}}, VALID_MAX_POWER, "H7"),
        # Edge case tests
        ("getDeviceInfo", None, None, "E1"),
        ("getAlarm", None, None, "E2"),
        ("getOutputData", None, None, "E3"),
        ("getMaxPower", None, None, "E4"),
        ("setOnOff", None, None, "E5"),
        ("setMaxPower", None, None, "E6"),
        # Error case tests
        ("setMaxPower", {"data": {"maxPower": INVALID_MAX_POWER}}, ValueError, "ERR1"),
    ],
    ids=lambda param: param[-1]
)
async def test_apsystems_ez1m_methods(endpoint, return_value, expected_result, test_id):
    # Arrange
    inverter = APsystemsEZ1M(VALID_IP, VALID_PORT, VALID_TIMEOUT)
    mock_request = AsyncMock(return_value=return_value)

    # Act
    with patch.object(inverter, '_request', new=mock_request):
        if isinstance(expected_result, type) and issubclass(expected_result, Exception):
            with pytest.raises(expected_result):
                await getattr(inverter, endpoint.replace("get", "get_").replace("set", "set_"))(VALID_MAX_POWER if "MaxPower" in endpoint else None)
        else:
            result = await getattr(inverter, endpoint.replace("get", "get_").replace("set", "set_"))(VALID_MAX_POWER if "MaxPower" in endpoint else None)

    # Assert
    if not isinstance(expected_result, type) or not issubclass(expected_result, Exception):
        assert result == expected_result
