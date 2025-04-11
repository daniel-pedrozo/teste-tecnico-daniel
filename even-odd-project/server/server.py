import asyncio
import json
from typing import Dict

import redis
from fastapi import FastAPI, HTTPException, Query
from nats.aio.client import Client as NATS
from pydantic_core import from_json

from server.logging_config import setup_logging
from server.models import (ClientIDModel, ClientRequest, EvenNumberResponse,
                           OddNumberResponse)

log = setup_logging()

r = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)

nats_address = "nats://nats-server:4222"
nats_even_subject = "get_even_service"
nats_odd_subject = "get_odd_service"

app = FastAPI()


async def publish_nats_message(subject: str, client_id: str) -> Dict:
    nc = NATS()
    try:
        await nc.connect(nats_address)
        payload = ClientIDModel(client_id=client_id).json().encode()
        reply = await nc.request(subject, payload, timeout=1)
        return from_json(reply.data.decode())
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=504, detail=f"Timeout waiting for {subject} response"
        )
    except json.JSONDecodeError as e:
        log.error(
            "Error decoding NATS response",
            error=str(e),
            raw_data=reply.data.decode(),
            subject=subject,
        )
        raise HTTPException(status_code=500, detail=f"Invalid response from {subject}")
    except Exception as e:
        log.error("Error communicating with NATS", error=str(e), subject=subject)
        raise HTTPException(
            status_code=500, detail=f"Error communicating with {subject}"
        )
    finally:
        await nc.close()


@app.get("/conection")
async def check_conection():
    return {"status": "conected to the server"}


@app.get("/get_even", response_model=EvenNumberResponse)
async def get_even_number(client_id: str = Query(...)):
    try:
        response = await publish_nats_message(nats_even_subject, client_id)
        if "error" in response:
            raise HTTPException(status_code=400, detail=response["error"])
        if "even_number" in response:
            return {"even_number": response["even_number"]}
        else:
            log.error("Unexpected response from even service", response=response)
            raise HTTPException(
                status_code=500, detail="Unexpected response from even service"
            )
    except HTTPException as e:
        raise e
    except Exception as e:
        log.error(
            "Error processing request for even number",
            error=str(e),
            client_id=client_id,
        )
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/get_odd", response_model=OddNumberResponse)
async def get_odd_number(client_id: str = Query(...)):
    try:
        response = await publish_nats_message(nats_odd_subject, client_id)
        if "error" in response:
            raise HTTPException(status_code=400, detail=response["error"])
        if "odd_number" in response:
            return {"odd_number": response["odd_number"]}
        else:
            log.error("Unexpected response from odd service", response=response)
            raise HTTPException(
                status_code=500, detail="Unexpected response from odd service"
            )
    except HTTPException as e:
        raise e
    except Exception as e:
        log.error(
            "Error processing request for odd number",
            error=str(e),
            client_id=client_id,
        )
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/last-number")
async def get_last_number(client_id: str = Query(...)):
    key = f"client:{client_id}:numbers"
    try:
        if not r.exists(key):
            raise HTTPException(status_code=404, detail="Client not found")

        last_number = r.lindex(key, 0)

        if last_number is None:
            raise HTTPException(
                status_code=404, detail="No numbers found for this client"
            )
        return {"client_id": client_id, "last_number": int(last_number)}

    except Exception as e:
        log.error("Failed to fetch last number", client_id=client_id, error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/get-history")
async def get_history(client_id: str = Query(...)):
    key = f"client:{client_id}:numbers"
    try:
        if not r.exists(key):
            raise HTTPException(status_code=404, detail="Client not found")

        number_history = r.lrange(key, 0, -1)

        if number_history is None:
            raise HTTPException(
                status_code=404, detail="No numbers found for this client"
            )
        return {"client_id": client_id, "number_history": (number_history)}

    except Exception as e:
        log.error("Failed to fetch last number", client_id=client_id, error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/register-client", response_model=ClientIDModel)
async def register_client(client_request: ClientRequest):
    key = f"client:{client_request.client_id}"
    try:
        if r.exists(key):
            log.bind(client_id=client_request.client_id).info(
                "client_already_registered"
            )
            raise HTTPException(status_code=400, detail="Client already registered")
        else:
            r.set(key, "registered")
            log.bind(client_id=client_request.client_id).info("client_registered")
            return {"client_id": client_request.client_id}

    except HTTPException as e:
        raise e
    except Exception as e:
        log.error(
            "Error processing client registration",
            error=str(e),
            client_id=client_request.client_id,
        )
        raise HTTPException(status_code=500, detail="Internal server error")
