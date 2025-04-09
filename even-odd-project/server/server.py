import asyncio
import json
from typing import Dict

import redis
import structlog
from fastapi import FastAPI, HTTPException
from nats.aio.client import Client as NATS
from pydantic import BaseModel

structlog.configure(
    processors=[
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.dev.ConsoleRenderer(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

log = structlog.get_logger(__name__)

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
nats_address = "nats://localhost:4222"
nats_even_subject = "get_even_service"
nats_odd_subject = "get_odd_service"

app = FastAPI()


class ClientRequest(BaseModel):
    client_id: str


class EvenNumberResponse(BaseModel):
    even_number: int


class OddNumberResponse(BaseModel):
    odd_number: int


class ClientIDModel(BaseModel):
    client_id: str


async def publish_nats_message(subject: str, client_id: str) -> Dict:
    nc = NATS()
    try:
        await nc.connect(nats_address)
        payload = ClientIDModel(client_id=client_id).json().encode()
        reply = await nc.request(
            subject, payload, timeout=1
        )  
        return json.loads(reply.data.decode())
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


@app.post("/get_even", response_model=EvenNumberResponse)
async def get_even_number(client_request: ClientRequest):
    try:
        response = await publish_nats_message(
            nats_even_subject, client_request.client_id
        )
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
            client_id=client_request.client_id,
        )
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/get_odd", response_model=OddNumberResponse)
async def get_odd_number(client_request: ClientRequest):
    try:
        response = await publish_nats_message(
            nats_odd_subject, client_request.client_id
        )
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
            client_id=client_request.client_id,
        )
        raise HTTPException(status_code=500, detail="Internal server error")
