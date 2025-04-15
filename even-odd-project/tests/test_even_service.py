import pytest
import json
from unittest.mock import AsyncMock, patch, MagicMock
from services.even_service.even_service import message_handler
from services.even_service.client_model import ClientIDModel


@pytest.mark.asyncio
async def test_valid_client(monkeypatch):
    # Setup mocks
    client_id = "test123"
    even_number = 42

    # Mock Redis
    mock_exists = AsyncMock(return_value=True)
    mock_lpush = AsyncMock()

    monkeypatch.setattr("services.even-service.even_service.r.exists", mock_exists)
    monkeypatch.setattr("services.even-service.even_service.r.lpush", mock_lpush)

    # Prepare a fake message with a valid client_id
    msg = AsyncMock()
    msg.data.decode.return_value = json.dumps({"client_id": client_id})

    # Run the handler
    await message_handler(msg)

    # Assertions
    mock_exists.assert_called_once_with(f"client:{client_id}")
    mock_lpush.assert_called_once()
    msg.respond.assert_called_once()
    response = json.loads(msg.respond.call_args[0][0].decode())
    assert "even_number" in response
    assert response["even_number"] % 2 == 0


@pytest.mark.asyncio
async def test_invalid_json():
    msg = AsyncMock()
    msg.data.decode.return_value = "invalid-json"

    await message_handler(msg)

    msg.respond.assert_called_once()
    response = json.loads(msg.respond.call_args[0][0].decode())
    assert "error" in response


@pytest.mark.asyncio
async def test_invalid_model_schema():
    msg = AsyncMock()
    msg.data.decode.return_value = json.dumps({"invalid_key": "value"})

    await message_handler(msg)

    msg.respond.assert_called_once()
    response = json.loads(msg.respond.call_args[0][0].decode())
    assert "error" in response


@pytest.mark.asyncio
async def test_unregistered_client(monkeypatch):
    client_id = "unregistered"
    msg = AsyncMock()
    msg.data.decode.return_value = json.dumps({"client_id": client_id})

    mock_exists = AsyncMock(return_value=False)
    monkeypatch.setattr("services.even-service.even_service.r.exists", mock_exists)

    await message_handler(msg)

    msg.respond.assert_called_once()
    response = json.loads(msg.respond.call_args[0][0].decode())
    assert "error" in response
    assert response["error"] == "Client not registered"
