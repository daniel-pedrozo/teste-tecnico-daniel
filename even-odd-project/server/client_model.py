from pydantic import BaseModel


class ClientIDModel(BaseModel):
    client_id: str
