from fastapi import FastAPI
from threading import Thread

from scraper.santander_scraper import SantanderScraper

app = FastAPI()


@app.get("/")
async def root():

    rut = "200719913"
    password = "46@8sA5uqV"
    scraper = SantanderScraper(rut, password, headles=False)
    scraper.scrap()

    return {"message": "Hello World"}
