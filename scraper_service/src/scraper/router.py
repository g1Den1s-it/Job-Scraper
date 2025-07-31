from fastapi import APIRouter


scraper = APIRouter()


@scraper.get('/list-work/')
async def list_work():
    pass

