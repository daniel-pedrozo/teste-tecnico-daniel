import asyncio
import json
import random

import redis
from nats.aio.client import Client as NATS
from pydantic import BaseModel, ValidationError


class ClientIDModel(BaseModel):
    client_id: str


client_data = {}

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


async def message_handler(msg):
    data = msg.data.decode()
    try:
        data_dict = json.loads(data)
        client = ClientIDModel(**data_dict)
    except (ValidationError, json.JSONDecodeError) as e:
        await msg.respond(json.dumps({"error": str(e)}).encode())
        return

    client_key = f"client:{client.client_id}:numbers"

    even_number = random.randint(1, 50) * 2
    r.lpush(client_key, even_number)

    response = {"even_number": even_number}

    await msg.respond(json.dumps(response).encode())


async def main():
    nc = NATS()
    await nc.connect("localhost:4222")
    await nc.subscribe("get_even_service", cb=message_handler)
    print("Service is listening for requests on 'get_even_service'")
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
