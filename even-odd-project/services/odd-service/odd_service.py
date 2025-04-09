import asyncio
import json
import random

import redis
from client_model import ClientIDModel
from nats.aio.client import Client as NATS
from pydantic import ValidationError
from structlog_config import config

log = config()

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


async def message_handler(msg):
    data = msg.data.decode()
    try:
        data_dict = json.loads(data)
        client = ClientIDModel(**data_dict)
    except (ValidationError, json.JSONDecodeError) as e:
        log.error("Invalid request data", error=str(e), raw_data=data)
        await msg.respond(json.dumps({"error": str(e)}).encode())
        return

    client_key = f"client:{client.client_id}"

    if not r.exists(client_key):
        log.warning(
            "Unregistered client tried to access odd service",
            client_id=client.client_id,
        )
        await msg.respond(json.dumps({"error": "Client not registered"}).encode())
        return

    number_key = f"{client_key}:numbers"
    odd_number = random.randint(1, 50) * 2 + 1
    r.lpush(number_key, odd_number)

    log.info("Odd number generated", client_id=client.client_id, odd_number=odd_number)

    await msg.respond(json.dumps({"odd_number": odd_number}).encode())


async def main():
    nc = NATS()
    await nc.connect("localhost:4222")
    await nc.subscribe("get_odd_service", cb=message_handler)
    log.info("Odd service listening on 'get_odd_service'")
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
