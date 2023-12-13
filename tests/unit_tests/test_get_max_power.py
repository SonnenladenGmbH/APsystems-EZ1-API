import pytest


@pytest.mark.parametrize(
    "test_id, output_data, expected",
    [
        ("happy-100", {"data": {"maxPower": "100"}}, 100),
        ("happy-200", {"data": {"maxPower": "200"}}, 200),
        ("happy-500", {"data": {"maxPower": "500"}}, 500),
    ],
)
@pytest.mark.asyncio
async def test_get_max_power_happy_path(test_id, output_data, expected, mock_response):
    # Arrange
    ez1m = mock_response(output_data)

    # Act
    result = await ez1m.get_max_power()

    # Assert
    assert result == expected, f"Test ID: {test_id}"


# Test cases for edge cases
@pytest.mark.parametrize(
    "test_id, output_data, expected",
    [
        ("edge-zero", {"data": {"maxPower": "0"}}, 0),
        ("edge-empty", {"data": {"maxPower": ""}}, None),
        ("edge-none", None, None),
    ],
)
@pytest.mark.asyncio
async def test_get_max_power_edge_cases(test_id, output_data, expected, mock_response):
    # Arrange
    ez1m = mock_response(output_data)

    # Act
    result = await ez1m.get_max_power()

    # Assert
    assert result == expected, f"Test ID: {test_id}"
