import pytest
from APsystemsEZ1 import ReturnOutputData


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "response_data, expected_output, test_id",
    [
        # Happy path tests with various realistic test values
        (
            {
                "data": {
                    "p1": 100.0,
                    "e1": 50.0,
                    "te1": 500.0,
                    "p2": 200.0,
                    "e2": 75.0,
                    "te2": 750.0,
                },
                "status": 0,
            },
            ReturnOutputData(
                p1=100.0, e1=50.0, te1=500.0, p2=200.0, e2=75.0, te2=750.0
            ),
            "happy_path_1",
        ),
        (
            {
                "data": {
                    "p1": 0.0,
                    "e1": 0.0,
                    "te1": 0.0,
                    "p2": 0.0,
                    "e2": 0.0,
                    "te2": 0.0,
                },
                "status": 0,
            },
            ReturnOutputData(p1=0.0, e1=0.0, te1=0.0, p2=0.0, e2=0.0, te2=0.0),
            "happy_path_2",
        ),
        # Edge cases
        (
            {
                "data": {
                    "p1": -1.0,
                    "e1": -1.0,
                    "te1": -1.0,
                    "p2": -1.0,
                    "e2": -1.0,
                    "te2": -1.0,
                },
                "status": 0,
            },
            ReturnOutputData(p1=-1.0, e1=-1.0, te1=-1.0, p2=-1.0, e2=-1.0, te2=-1.0),
            "edge_case_negative_values",
        ),
    ],
)
async def test_get_output_data_happy_paths(
    response_data, expected_output, test_id, mock_response
):
    # Arrange
    ez1m = mock_response(response_data)

    # Act
    result = await ez1m.get_output_data()

    # Assert
    assert result == expected_output


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "response_data, test_id",
    [
        # Error cases
        ({"data": {}, "status": 0}, "error_case_empty_data"),
    ],
)
async def test_get_output_data_error_nulled_data(response_data, test_id, mock_response):
    # Arrange
    ez1m = mock_response(response_data)

    # Assert
    data = await ez1m.get_output_data()
    assert data == ReturnOutputData(p1=0.0, e1=0.0, te1=0.0, p2=0.0, e2=0.0, te2=0.0)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "response_data, test_id",
    [
        # Error cases
        (None, "error_case_none_response"),
    ],
)
async def test_get_output_data_error_no_response(response_data, test_id, mock_response):
    # Arrange
    ez1m = mock_response(response_data)

    # Act
    result = await ez1m.get_output_data()

    # Assert
    assert result is None
