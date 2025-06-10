import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from aiohttp import ClientSession
from APsystemsEZ1 import APsystemsEZ1M, InverterReturnedError

@pytest.fixture
def ez1m():
    return APsystemsEZ1M(ip_address="0.0.0.0")

@pytest.fixture
def success_response_data():
    return {"message": "SUCCESS", "data": {"test": "data"}}

@pytest.fixture
def mock_response_success(success_response_data):
    return AsyncMock(status=200, json=AsyncMock(return_value=success_response_data))

@pytest.fixture
def mock_response_failure():
    return AsyncMock(status=200, json=AsyncMock(return_value={"message": "FAILED"}))


def _create_mock_session(return_value):
    mock_session = MagicMock()
    if isinstance(return_value, list):
        mock_session.get.return_value.__aenter__.side_effect = return_value
    else:
        mock_session.get.return_value.__aenter__.return_value = return_value
    mock_session.close = AsyncMock()

    return mock_session

@pytest.mark.asyncio
async def test_request_retry_success_first_attempt(ez1m, mock_response_success, success_response_data):
    # Arrange
    mock_session = _create_mock_session(mock_response_success)

    # Act
    with patch.object(ClientSession, '__new__', return_value=mock_session):
        result = await ez1m._request("test_endpoint", retry=3)

    # Assert
    assert result == success_response_data
    assert mock_session.get.call_count == 1


@pytest.mark.asyncio
async def test_request_retry_success_after_retry(ez1m, mock_response_failure, mock_response_success, success_response_data):
    # Arrange
    mock_session = _create_mock_session([mock_response_failure, mock_response_success])

    # Act
    with patch.object(ClientSession, '__new__', return_value=mock_session):
        result = await ez1m._request("test_endpoint", retry=3)

    # Assert
    assert result == success_response_data
    assert mock_session.get.call_count == 2


@pytest.mark.asyncio
async def test_request_retry_exhausted(ez1m, mock_response_failure):
    # Arrange
    mock_session = _create_mock_session(mock_response_failure)

    # Act
    retry_count = 4
    with patch.object(ClientSession, '__new__', return_value=mock_session):
        with pytest.raises(InverterReturnedError):
            await ez1m._request("test_endpoint", retry=retry_count)

    # Assert
    assert mock_session.get.call_count == 1 + retry_count  # Initial call + retries
