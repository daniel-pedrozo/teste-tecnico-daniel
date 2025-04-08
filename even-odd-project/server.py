import asyncio
import json
import logging
import sys

import redis
import structlog
from flask import Flask, jsonify, request
from nats.aio.client import Client as NATS
from pydantic import BaseModel, ValidationError

# --------------------
# Structlog Setup
# --------------------
logging.basicConfig(
    format="%(message)s",
    stream=sys.stdout,
    level=logging.INFO,
)

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    cache_logger_on_first_use=True,
)

log = structlog.get_logger()

# --------------------
# Flask App Setup
# --------------------
app = Flask(__name__)
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


# Pydantic model
class ClientIDModel(BaseModel):
    client_id: str
    new_data: int | None = None


@app.route("/connection", methods=["GET"])
def conection():
    log.info("health_check")
    return jsonify({"message": "Connected to the server"}), 200


def validate_and_log_client(json_data, route_name):
    try:
        data = ClientIDModel(**json_data)
        log.bind(client_id=data.client_id).info(
            route_name, action="request_received", data=json_data
        )
        return data
    except ValidationError as e:
        log.warning(route_name, error="Validation failed", details=str(e))
        return None


@app.route("/get-even", methods=["POST"])
def get_even():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "Invalid JSON"}), 400

    data = validate_and_log_client(json_data, "get_even")
    if not data:
        return jsonify({"error": "Invalid client_id or data"}), 400

    async def send_request():
        nc = NATS()
        await nc.connect("localhost:4222")
        payload = json_data.copy()
        payload["client_id"] = data.client_id
        response = await nc.request(
            "get_even_service", json.dumps(payload).encode(), timeout=5
        )
        await nc.close()
        return response.data

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        reply = loop.run_until_complete(send_request())
        log.bind(client_id=data.client_id).info(
            "get_even_response", response=reply.decode()
        )
        return jsonify(json.loads(reply.decode())), 200
    except Exception as e:
        log.error("get_even_error", error=str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/get-odd", methods=["POST"])
def get_odd():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "Invalid JSON"}), 400

    data = validate_and_log_client(json_data, "get_odd")
    if not data:
        return jsonify({"error": "Invalid client_id or data"}), 400

    async def send_request():
        nc = NATS()
        await nc.connect("localhost:4222")
        payload = json_data.copy()
        payload["client_id"] = data.client_id
        response = await nc.request(
            "get_odd_service", json.dumps(payload).encode(), timeout=5
        )
        await nc.close()
        return response.data

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        reply = loop.run_until_complete(send_request())
        log.bind(client_id=data.client_id).info(
            "get_odd_response", response=reply.decode()
        )
        return jsonify(json.loads(reply.decode())), 200
    except Exception as e:
        log.error("get_odd_error", error=str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/pass-ident", methods=["POST"])
def save_ident():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "Invalid JSON"}), 400

    data = validate_and_log_client(json_data, "pass_ident")
    if not data:
        return jsonify({"error": "Invalid client_id"}), 400

    key = f"client:{data.client_id}"
    if not r.exists(key):
        r.set(key, "registered")
        log.bind(client_id=data.client_id).info("client_registered")
        return jsonify(
            {"message": f"Client {data.client_id} registered successfully"}
        ), 200
    else:
        log.bind(client_id=data.client_id).info("client_already_registered")
        return jsonify({"message": f"Client {data.client_id} already exists"}), 200


@app.route("/get-last-number", methods=["POST"])
def get_last_number():
    try:
        data = ClientIDModel(**request.get_json())
    except ValidationError as e:
        log.warning("get_last_number", error="Validation failed", details=str(e))
        return jsonify({"error": str(e)}), 400

    key = f"client:{data.client_id}:numbers"

    if not r.exists(key):
        log.warning(
            "get_last_number", client_id=data.client_id, error="Client ID not found"
        )
        return jsonify({"error": "Client ID not found"}), 404

    last_number = r.lindex(key, 0)
    if last_number:
        log.info("get_last_number", client_id=data.client_id, number=last_number)
        return jsonify({"last_number": int(last_number)}), 200
    else:
        log.info("get_last_number_empty", client_id=data.client_id)
        return jsonify({"error": "No numbers stored for this client"}), 404


@app.route("/get-history", methods=["POST"])
def get_history():
    try:
        data = ClientIDModel(**request.get_json())
    except ValidationError as e:
        log.warning("get_history", error="Validation failed", details=str(e))
        return jsonify({"error": str(e)}), 400

    key = f"client:{data.client_id}:numbers"
    if not r.exists(key):
        log.warning(
            "get_history", client_id=data.client_id, error="Client ID not found"
        )
        return jsonify({"error": "Client ID not found"}), 404

    number_history = r.lrange(key, 0, -1)
    if number_history:
        log.info("get_history", client_id=data.client_id, history=number_history)
        return jsonify({"number_history": [int(num) for num in number_history]}), 200
    else:
        log.info("get_history_empty", client_id=data.client_id)
        return jsonify({"error": "No numbers stored for this client"}), 404


if __name__ == "__main__":
    app.run()
