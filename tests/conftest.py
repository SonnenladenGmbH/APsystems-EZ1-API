import pytest
import APsystemsEZ1
from unittest.mock import AsyncMock
from typing import Any

@pytest.fixture(scope="function")
def mock_response():
    def inner(return_values: Any) -> APsystemsEZ1.APsystemsEZ1M:
        ez1m = APsystemsEZ1.APsystemsEZ1M(ip_address="0.0.0.0")
        ez1m._request = AsyncMock(return_value=return_values)
        return ez1m
    yield inner
