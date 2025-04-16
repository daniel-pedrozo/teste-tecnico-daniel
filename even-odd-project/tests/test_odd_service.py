import json
import pytest
from unittest.mock import AsyncMock
from services.odd_service.odd_service import message_handler


@pytest.mark.asyncio
async def test_valid_client(monkeypatch):
    client_id = "test123"

    mock_exists = AsyncMock(return_value=True)
    mock_lpush = AsyncMock()

    monkeypatch.setattr("services.odd_service.odd_service.r.exists", mock_exists)
    monkeypatch.setattr("services.odd_service.odd_service.r.lpush", mock_lpush)

    msg = AsyncMock()
    msg.data = json.dumps({"client_id": client_id}).encode("utf-8")

    await message_handler(msg)

    mock_exists.assert_awaited_once_with(f"client:{client_id}")
    mock_lpush.assert_awaited()


@pytest.mark.asyncio
async def test_invalid_json():
    msg = AsyncMock()
    msg.data = b"invalid-json"

    await message_handler(msg)


@pytest.mark.asyncio
async def test_invalid_model_schema():
    msg = AsyncMock()
    msg.data = json.dumps({"invalid_key": "value"}).encode("utf-8")

    
    await message_handler(msg)


@pytest.mark.asyncio
async def test_unregistered_client(monkeypatch):
    client_id = "unregistered"

    mock_exists = AsyncMock(return_value=False)
    monkeypatch.setattr("services.odd_service.odd_service.r.exists", mock_exists)

    msg = AsyncMock()
    msg.data = json.dumps({"client_id": client_id}).encode("utf-8")

    await message_handler(msg)

    mock_exists.assert_awaited_once_with(f"client:{client_id}")
