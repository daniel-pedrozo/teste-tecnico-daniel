import asyncio
import json
import random

import redis.asyncio as redis

from nats.aio.client import Client as NATS
from pydantic import ValidationError
from structlog_config import config
from client_model import ClientIDModel, EvenNumberResponse, ErrorResponse

log = config()

r = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)


async def message_handler(msg):
    data = msg.data.decode()
    try:
        data_dict = json.loads(data)
        client = ClientIDModel(**data_dict)
    except (ValidationError, json.JSONDecodeError) as e:
        log.error("Invalid request data", error=str(e), raw_data=data)
        error_response = ErrorResponse(error=str(e))
        await msg.respond(error_response.model_dump_json().encode())  
        return

    client_key = f"client:{client.client_id}"

    if not await r.exists(client_key):
        log.warning(
            "Unregistered client tried to access even service",
            client_id=client.client_id,
        )
        error_response = ErrorResponse(error="Client not registered")
        await msg.respond(error_response.model_dump_json().encode())
        return

    number_key = f"{client_key}:numbers"
    even_number = random.choice(range(0, 101, 2))
    await r.lpush(number_key, even_number)

    log.info(
        "Even number generated", client_id=client.client_id, even_number=even_number
    )

    even_number_response = EvenNumberResponse(even_number=even_number)
    await msg.respond(even_number_response.model_dump_json().encode())


async def main():
    nc = NATS()
    await nc.connect("nats://nats-server:4222")
    await nc.subscribe("get_even_service", cb=message_handler)
    log.info("Even service listening on 'get_even_service'")
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
