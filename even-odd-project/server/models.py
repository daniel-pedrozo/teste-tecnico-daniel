from pydantic import BaseModel


class ClientRequest(BaseModel):
    client_id: str


class EvenNumberResponse(BaseModel):
    even_number: int


class OddNumberResponse(BaseModel):
    odd_number: int


class ClientIDModel(BaseModel):
    client_id: str
