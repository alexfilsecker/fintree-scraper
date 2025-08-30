from fastapi import FastAPI, Response
import os

from models.credentials import SantanderCredentials, CommonWealthCredentials, FalabellaCredentials

from scrapers.santander import scrap_santander
from scrapers.commonwealth import scrap_commonwealth
from scrapers.falabella import FalabellaScraper
from logger import logger


in_container = os.environ.get("IN_CONTAINER", "false") == "true"

app = FastAPI()


@app.get("/")
async def hello_world():
    return {"message": "Hello World"}


@app.post("/santander")
async def post_santander(credentials: SantanderCredentials):
    movements = scrap_santander(
        credentials.rut, credentials.password, headless=in_container
    )
    return movements


@app.post("/common-wealth")
async def post_common_wealth(credentials: CommonWealthCredentials):
    total_pending, pending_movements, non_pending_movements = scrap_commonwealth(
        credentials.client_number, credentials.password, headless=in_container
    )

    return {
        "pending": {
            "total": total_pending,
            "movements": pending_movements,
        },
        "non_pending": non_pending_movements,
    }

@app.post("/falabella")
async def post_banco_falabella(credentials: FalabellaCredentials): 
    print("scraping falabella")
    try:
        url = "https://www.bancofalabella.cl/"
        result = FalabellaScraper(url, in_container, credentials).scrap()
        return result
    except Exception as e:
        return Response(
            content=f"An error occurred: {e}",
            status_code=500
        )

if __name__ == "__main__":
    import uvicorn

    if in_container:
        port = 8080
    else:
        port = 8000

    uvicorn.run(app="main:app", host="0.0.0.0", port=port, reload=True)
