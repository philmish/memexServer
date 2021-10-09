from typing import List, Dict
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from memexIndexer.api.client import Client
from memexIndexer.indexer.schemas import Query
from memexIndexer.utils.http import parse_HTTPResponse
from memexIndexer.api.routers.bookmarks.schemas import (
    BookmarkBase,
    BookmarkFromDB,
    BookmarkFulltextQuery,
    BookmarkQuery
)


router = APIRouter(
    prefix="/bookmarks",
    tags=["bookmarks"]
)


@router.get("/ping")
def ping():
    return "Hello World, this is the bookmarks endpoint."


@router.get(
    "/all",
    response_model=List[BookmarkFromDB]
    )
def all_bookmarks():
    client = Client()
    resp = parse_HTTPResponse(
        client.get_all(
            item_type="bookmark"
            )
        )
    return [BookmarkFromDB(**data) for data in resp]


@router.post(
    "/get/id",
    response_model=Dict[str, str]
    )
def get_id(query: BookmarkQuery):
    client = Client()
    resp = parse_HTTPResponse(
        client.get_id(
            query=query
            )
        )
    return resp


@router.get(
    "/{item_id}",
    response_model=BookmarkFromDB
    )
def get_by_id(item_id: str):
    client = Client()
    resp = parse_HTTPResponse(
        client.get_by_id(
            query=Query(
                item_type="bookmark",
                data=item_id
            )
        )
    )
    return BookmarkFromDB(**resp)


@router.post(
    "/create",
    response_model=BookmarkFromDB
    )
def create_bookmark(item: BookmarkBase):
    client = Client()
    resp = parse_HTTPResponse(
        client.create(
            data=item
            )
        )
    return BookmarkFromDB(**resp)


@router.post(
    "/query",
    response_model=List[BookmarkFromDB]
    )
def query(query: BookmarkQuery):
    client = Client()
    resp = parse_HTTPResponse(
        client.read(
            query=query
            )
        )
    res = [BookmarkFromDB(**data) for data in resp]
    


@router.post(
    "/update/{item_id}",
    response_model=BookmarkFromDB
    )
def update(query: BookmarkQuery, item_id: str):
    client = Client()
    resp = parse_HTTPResponse(
        client.update(
            item_id=item_id,
            query=query
            )
        )
    return BookmarkFromDB(**resp)


@router.post(
    "/delete/{item_id}",
    response_model=BookmarkFromDB
    )
def delete_item(item_id: str):
    client = Client()
    resp = parse_HTTPResponse(
        client.delete(
            item_id=item_id,
            item_type="bookmark"
            )
        )
    return BookmarkFromDB(**resp)


@router.post(
    "/fulltext",
    response_model=List[BookmarkFromDB]
    )
def fulltext_search(query: BookmarkFulltextQuery):
    client = Client()
    resp = parse_HTTPResponse(
        client.fulltext_search(
            query=query
            )
        )
    return [BookmarkFromDB(**data) for data in resp]
