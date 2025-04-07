import asyncio
import json

import redis
from flask import Flask, jsonify, request
from nats.aio.client import Client as NATS
from pydantic import BaseModel, ValidationError

app = Flask(__name__)

client_data = {}

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


# Pydantic models for request validation
class ClientIDModel(BaseModel):
    client_id: str  # Ensuring client_id is always a string
    new_data: int | None = None  # Ensuring data is always a integer or none


@app.route("/connection", methods=["GET"])
def conection():
    return jsonify({"message": "Connected to the server"}), 200


@app.route("/get-even", methods=["POST"])
def get_even():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "Invalid JSON"}), 400

    try:
        data = ClientIDModel(**json_data)
        client_id = data.client_id
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

    async def send_request():
        nc = NATS()
        await nc.connect("localhost:4222")
        payload = json_data.copy()
        payload["client_id"] = client_id
        response = await nc.request(
            "get_even_service", json.dumps(payload).encode(), timeout=5
        )
        await nc.close()
        return response.data

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        reply = loop.run_until_complete(send_request())
        return jsonify(json.loads(reply.decode())), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/get-odd", methods=["POST"])
def get_odd():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "Invalid JSON"}), 400

    try:
        data = ClientIDModel(**json_data)
        client_id = data.client_id
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

    async def send_request():
        nc = NATS()
        await nc.connect("localhost:4222")
        payload = json_data.copy()
        payload["client_id"] = client_id
        response = await nc.request(
            "get_odd_service", json.dumps(payload).encode(), timeout=5
        )
        await nc.close()
        return response.data

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        reply = loop.run_until_complete(send_request())
        return jsonify(json.loads(reply.decode())), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/pass-ident", methods=["POST"])
def save_ident():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "Invalid JSON"}), 400

    try:
        data = ClientIDModel(**json_data)
        client_id = data.client_id
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

    key = f"client:{client_id}"
    if not r.exists(key):
        r.set(key, "registered")  # Just a marker
        return jsonify({"message": f"Client {client_id} registered successfully"}), 200
    else:
        return jsonify({"message": f"Client {client_id} already exists"}), 200


@app.route("/get-last-number", methods=["POST"])
def get_last_number():
    try:
        data = ClientIDModel(**request.get_json())
        client_id = data.client_id
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

    key = f"client:{client_id}:numbers"

    if not r.exists(key):
        return jsonify({"error": "Client ID not found"}), 404

    last_number = r.lindex(key, 0)

    if last_number:
        return jsonify({"last_number": int(last_number)}), 200
    else:
        return jsonify({"error": "No numbers stored for this client"}), 404


@app.route("/get-history", methods=["POST"])
def get_history():
    """Retrieve the full number history for a given client."""
    try:
        data = ClientIDModel(**request.get_json())
        client_id = data.client_id
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

    key = f"client:{client_id}:numbers"

    if not r.exists(key):
        return jsonify({"error": "Client ID not found"}), 404

    number_history = r.lrange(key, 0, -1)  # Get full list
    if number_history:
        return jsonify({"number_history": [int(num) for num in number_history]}), 200
    else:
        return jsonify({"error": "No numbers stored for this client"}), 404


if __name__ == "__main__":
    app.run()
