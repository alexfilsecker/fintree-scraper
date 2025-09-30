from fastapi import FastAPI, Response
import os

from models.credentials import FalabellaCredentials

from scrapers.falabella import FalabellaScraper


in_container = os.environ.get("IN_CONTAINER", "false") == "true"

app = FastAPI()


@app.get("/")
async def hello_world():
    return {"message": "Hello World"}

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
