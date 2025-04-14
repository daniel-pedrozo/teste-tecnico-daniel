from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from server.server import app

client = TestClient(app)


def test_conection_endpoint():
    response = client.get("/conection")
    assert response.status_code == 200
    assert response.json() == {"status": "conected to the server"}


@patch("server.server.publish_nats_message", new_callable=AsyncMock)
def test_get_even_endpoint(mock_publish):
    mock_publish.return_value = {"even_number": 2}
    client_id = "test_client"
    response = client.get(f"/get_even?client_id={client_id}")
    assert response.status_code == 200
    assert response.json() == {"even_number": 2}


@patch("server.server.publish_nats_message", new_callable=AsyncMock)
def test_get_odd_endpoint(mock_publish):
    mock_publish.return_value = {"odd_number": 3}
    client_id = "test_client"
    response = client.get(f"/get_odd?client_id={client_id}")
    assert response.status_code == 200
    assert response.json() == {"odd_number": 3}


@patch("server.server.r")
def test_get_last_number_endpoint(mock_redis):
    mock_redis.exists.return_value = True
    mock_redis.lindex.return_value = 8
    client_id = "test_client"
    response = client.get(f"/last-number?client_id={client_id}")
    assert response.status_code == 200
    assert response.json() == {"client_id": client_id, "last_number": 8}


@patch("server.server.r")
def test_get_history_endpoint(mock_redis):
    mock_redis.exists.return_value = True
    mock_redis.lrange.return_value = [2, 4, 6]
    client_id = "test_client"
    response = client.get(f"/get-history?client_id={client_id}")
    assert response.status_code == 200
    assert response.json() == {"client_id": client_id, "number_history": [2, 4, 6]}


@patch("server.server.r")
def test_register_client_success(mock_redis):
    mock_redis.exists.return_value = False
    mock_redis.set.return_value = True
    client_id = "test_client"
    response = client.post("/register-client", json={"client_id": client_id})
    assert response.status_code == 200
    assert response.json() == {"client_id": client_id}


@patch("server.server.r")
def test_register_client_already_exists(mock_redis):
    mock_redis.exists.return_value = True
    client_id = "existing_client"
    response = client.post("/register-client", json={"client_id": client_id})
    assert response.status_code == 400
    assert response.json() == {"detail": "Client already registered"}
