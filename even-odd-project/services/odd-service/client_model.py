from pydantic import BaseModel


class ClientIDModel(BaseModel):
    client_id: str

class OddNumberResponse(BaseModel):
    odd_number: int

class ErrorResponse(BaseModel):
    error: str
