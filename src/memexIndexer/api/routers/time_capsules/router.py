from typing import List
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from memexIndexer.api.client import Client
from memexIndexer.indexer.schemas import Query
from memexIndexer.utils.http import parse_HTTPResponse
from memexIndexer.api.routers.time_capsules.schemas import (
    TimeCapsuleBase,
    TimeCapsuleDB,
    TimeCapsuleQuery
)


# TODO Add scraping and storing functionlity
router = APIRouter(
    prefix="/time_capsule",
    tags=["time_capsule"]
)


@router.get(
    "/all",
    response_model=List[TimeCapsuleDB])
def all_capsules():
    client = Client()
    resp = parse_HTTPResponse(
        client.get_all(
            item_type="time_capsule"
        )
    )
    return [TimeCapsuleDB(**data) for data in resp]


@router.post(
    "/create",
    response_model=TimeCapsuleDB
    )
def create_capsule(item: TimeCapsuleBase):
    # TODO Write archiving and file_path utilities for scraping and storing
    client = Client()
    resp = parse_HTTPResponse(
        client.create(
            data=item
            )
        )
    return TimeCapsuleDB(**resp)


@router.post(
    "/query",
    response_model=List[TimeCapsuleDB]
    )
def query(query: TimeCapsuleQuery):
    client = Client()
    resp = parse_HTTPResponse(
        client.read(
            query=query
            )
        )
    res = [TimeCapsuleDB(**data) for data in resp]
    if len(res) == 0:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
            )
    return res
    

@router.post(
    "/update/{item_id}",
    response_model=TimeCapsuleDB
    )
def update(query: TimeCapsuleQuery, item_id: str):
    client = Client()
    resp = parse_HTTPResponse(
        client.update(
            item_id=item_id,
            query=query
            )
        )
    return TimeCapsuleDB(**resp)


@router.post(
    "/delete/{item_id}",
    response_model=TimeCapsuleDB
    )
def delete_item(item_id: str):
    client = Client()
    resp = parse_HTTPResponse(
        client.delete(
            item_id=item_id,
            item_type="time_capsule"
            )
        )
    return TimeCapsuleDB(**resp)


@router.post(
    "/fulltext",
    response_model=List[TimeCapsuleDB])
def fulltext_search(query: Query):
    client = Client()
    resp = parse_HTTPResponse(
        client.fulltext_search(
            query=query
            )
        )
    return [TimeCapsuleDB(**data) for data in resp]
