import pytest
import APsystemsEZ1
from unittest.mock import AsyncMock


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "power_limit, expected",
    [
        (30, 30),  # ID: test-happy-path-lower-bound
        (400, 400),  # ID: test-happy-path-mid-value
        (800, 800),  # ID: test-happy-path-upper-bound
    ],
)
async def test_set_max_power_happy_path(power_limit, expected):
    # Act
    apsystem = APsystemsEZ1.APsystemsEZ1M(ip_address="0.0.0.0")
    apsystem._request = AsyncMock(return_value={"data": {"maxPower": power_limit}})
    result = await apsystem.set_max_power(power_limit)

    # Assert
    assert (
        result == expected
    ), f"Expected max power to be set to {expected}, but got {result}"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "power_limit, expected_exception, expected_message",
    [
        (
            29,
            ValueError,
            "Invalid setMaxPower value: expected int between '30' and '800', got '29'",
        ),  # ID: test-error-below-lower-bound
        (
            801,
            ValueError,
            "Invalid setMaxPower value: expected int between '30' and '800', got '801'",
        ),  # ID: test-error-above-upper-bound
        (
            "100",
            TypeError,
            "'<=' not supported between instances of 'int' and 'str'",
        ),  # ID: test-error-non-int-value
        (
            None,
            TypeError,
            "'<=' not supported between instances of 'int' and 'NoneType'",
        ),  # ID: test-error-none-value
    ],
)
async def test_set_max_power_error_cases(
    power_limit, expected_exception, expected_message
):
    # Arrange
    apsystem = APsystemsEZ1.APsystemsEZ1M(ip_address="0.0.0.0")
    apsystem._request = AsyncMock(return_value={"data": {"maxPower": power_limit}})

    # Act & Assert
    with pytest.raises(expected_exception) as exc_info:
        await apsystem.set_max_power(power_limit)
    assert (
        str(exc_info.value) == expected_message
    ), f"Expected error message to be '{expected_message}', but got '{str(exc_info.value)}'"
