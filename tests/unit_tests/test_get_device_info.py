import pytest
from APsystemsEZ1 import ReturnDeviceInfo


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "response_data, expected_result, test_id",
    [
        # Happy path tests with various realistic test values
        (
            {
                "data": {
                    "deviceId": "12345",
                    "devVer": "1.0",
                    "ssid": "Home_Network",
                    "ipAddr": "192.168.1.2",
                    "minPower": 100,
                    "maxPower": 1000,
                }, "status": 0
            },
            ReturnDeviceInfo(
                deviceId="12345",
                devVer="1.0",
                ssid="Home_Network",
                ipAddr="192.168.1.2",
                minPower=100,
                maxPower=1000,
            ),
            "happy_path_1",
        ),
        # Edge cases
        (
            {
                "data": {
                    "deviceId": "",
                    "devVer": "",
                    "ssid": "",
                    "ipAddr": "",
                    "minPower": 0,
                    "maxPower": 0,
                }, "status": 0
            },
            ReturnDeviceInfo(
                deviceId="", devVer="", ssid="", ipAddr="", minPower=0, maxPower=0
            ),
            "edge_case_empty_strings_and_zeros",
        ),
        # Error cases
        (None, None, "error_case_none_response"),
    ],
)
async def test_get_device_info(response_data, expected_result, test_id, mock_response):
    # Arrange
    ez1m = mock_response(response_data)

    # Act
    result = await ez1m.get_device_info()

    # Assert
    assert result == expected_result, f"Failed test case: {test_id}"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "response_data, test_id",
    [
        # Error cases
        (
            {"data": {}, "status": 0},
            "error_case_empty_data",
        ),
    ],
)
async def test_get_device_info_empty_data(response_data, test_id, mock_response):
    # Arrange
    ez1m = mock_response(response_data)

    # Assert
    with pytest.raises(TypeError) as exc_info:
        await ez1m.get_device_info()
    assert "missing 6 required positional arguments" in str(
        exc_info.value
    ), f"Test Failed: {test_id}"
