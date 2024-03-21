from fastapi import FastAPI
from threading import Thread

from scraper.scrap import scrap

app = FastAPI()


@app.get("/")
async def root():

    rut = "200719913"
    password = "46@8sA5uqV"

    t = Thread(target=scrap, args=(rut, password))
    t.start()

    return {"message": "Hello World"}
