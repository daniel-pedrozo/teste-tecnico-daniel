from pydantic import BaseModel


class ClientIDModel(BaseModel):
    client_id: str

class EvenNumberResponse(BaseModel):
    even_number: int

class ErrorResponse(BaseModel):
    error: str
