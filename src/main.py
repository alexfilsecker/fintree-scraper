from fastapi import FastAPI

from .routers.scrap_router import scrap_router

app = FastAPI()

app.include_router(scrap_router, prefix="/scrap")
