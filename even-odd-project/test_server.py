from fastapi.testclient import TestClient

from server.server import app

client = TestClient(app)

# Test is not working correctlly 

def test_conection_endpoint():
    response = client.get("/conection")
    assert response.status_code == 200
    assert response.json() == {"status": "conected to the server"}


def test_get_even_endpoint():
    client_id = "test_client"
    response = client.get(f"/get_even?client_id={client_id}")
    assert response.status_code == 200
    assert "even_number" in response.json()
    assert isinstance(response.json()["even_number"], int)


def test_get_odd_endpoint():
    client_id = "test_client"
    response = client.get(f"/get_odd?client_id={client_id}")
    assert response.status_code == 200
    assert "odd_number" in response.json()
    assert isinstance(response.json()["odd_number"], int)


def test_get_last_number_endpoint():
    client_id = "test_client"
    response = client.get(f"/last-number?client_id={client_id}")
    assert response.status_code == 404


def test_get_history_endpoint():
    client_id = "test_client"
    response = client.get(f"/get-history?client_id={client_id}")
    assert response.status_code == 404


def test_register_client_endpoint():
    client_id = "test_client"
    response = client.post("/register-client", json={"client_id": client_id})
    assert response.status_code == 200
    assert response.json() == {"client_id": client_id}

    response_duplicate = client.post("/register-client", json={"client_id": client_id})
    assert response_duplicate.status_code == 400
    assert response_duplicate.json() == {"detail": "Client already registered"}
