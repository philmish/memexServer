from typing import List
from fastapi import APIRouter, HTTPException
from pymongo import response
from memexIndexer.api.client import Client
from memexIndexer.api.rake_client import RakeClient
from memexIndexer.api.routers.scraped_data.schemas import ScrapeRequest, ScrapedDataDB
from memexIndexer.utils.http import parse_HTTPResponse

router = APIRouter(
    prefix="/scraping",
    tags=["scraping"]
)


@router.get("/ping")
def ping():
    return "Hello World, from the scraping enpoint"


@router.post("/rake", response_model=ScrapedDataDB)
def rake(req: ScrapeRequest):
    """Sends a scrape request to a rake api. Indexes and stores the incoming data"""
    rake_cli = RakeClient()
    db_cli = Client()
    response_data = rake_cli.make_request(req)
    if response_data["status_code"] == 200:
        resp = parse_HTTPResponse(
            db_cli.create(
                data=response_data
            )
        )
        return ScrapedDataDB(**resp)
    else:
        raise HTTPException(
            status_code=response_data["status_code"],
            detail=response_data["data"]
        )

@router.get("/plugins", response_model=List[str])
def plugins():
    """Returns all available plugins from the rake server."""
    rake_cli = RakeClient()
    results = rake_cli.all_plugins()
    return results

@router.get("/all", response_model=List[ScrapedDataDB])
def get_all():
    client = Client()
    resp = parse_HTTPResponse(
        client.get_all(
            item_type="scraped_data"
        )
    )
    return [ScrapedDataDB(**data) for data in resp]
