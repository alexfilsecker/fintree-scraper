from fastapi import APIRouter, Body
from datetime import date, datetime
from typing import List

from ..scraper.santander_scraper import SantanderScraper

scrap_router = APIRouter()


@scrap_router.post("/santander")
async def scrap_santander(rut: str = Body(...), password: str = Body(...)):

    print("SCRAPING")

    scraped_movements = SantanderScraper(rut, password).scrap()

    return scraped_movements
