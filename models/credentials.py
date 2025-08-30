from pydantic import BaseModel


class SantanderCredentials(BaseModel):
    rut: str
    password: str


class CommonWealthCredentials(BaseModel):
    client_number: str
    password: str


class FalabellaCredentials(BaseModel):
    rut: str
    password: str
