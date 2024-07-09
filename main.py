from fastapi import FastAPI
from pydantic import BaseModel

from scrapers.santander import scrap_santander
from scrapers.commonwealth import scrap_commonwealth

app = FastAPI()


class SantanderCredentials(BaseModel):
    rut: str
    password: str


class CommonWealthCredentials(BaseModel):
    client_number: str
    password: str


@app.get("/")
async def hello_world():
    return {"message": "Hello World"}


@app.post("/santander")
async def post_santander(credentials: SantanderCredentials):
    movements = scrap_santander(credentials.rut, credentials.password, headless=False)
    return movements


@app.post("/common-wealth")
async def post_common_wealth(credentials: CommonWealthCredentials):
    total_pending, pending_movements, non_pending_movements = scrap_commonwealth(
        credentials.client_number, credentials.password, headless=True
    )

    return {
        "pending": {
            "total": total_pending,
            "movements": pending_movements,
        },
        "non_pending": non_pending_movements,
    }
