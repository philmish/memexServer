from typing import List
from fastapi import APIRouter
from pymongo import response
from memexIndexer.api.client import Client
from memexIndexer.api.routers.scraped_data.schemas import ScrapedDataDB
from memexIndexer.utils.http import parse_HTTPResponse

router = APIRouter(
    prefix="/scraping",
    tags=["scraping"]
)


@router.get("/ping")
def ping():
    return "Hello World, from the scraping enpoint"

@router.get("/all", response_model=List[ScrapedDataDB])
def get_all():
    client = Client()
    resp = parse_HTTPResponse(
        client.get_all(
            item_type="scraped_data"
        )
    )