from typing import List, Dict
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from memexIndexer.api.client import Client
from memexIndexer.utils.http import parse_HTTPResponse
from memexIndexer.api.routers.books.schemas import BookBase, BookDB, BookQuery
from memexIndexer.indexer.schemas import Query


router = APIRouter(
    prefix="/books",
    tags=["books"]
)


@router.get("/ping")
def ping():
    return "Hello World, this is the books endpoint."


@router.get(
    "/all",
    response_model=List[BookDB]
    )
def all_notes():
    client = Client()
    resp = parse_HTTPResponse(
        client.get_all(
            item_type="books"
            )
        )
    return [BookDB(**data) for data in resp]


@router.post(
    "/get/id",
    response_model=Dict[str, str]
    )
def get_id(query: BookQuery):
    client = Client()
    resp = parse_HTTPResponse(
        client.get_id(
            query=query
            )
        )
    return resp


@router.post(
    "/create",
    response_model=BookDB
    )
def create_note(item: BookBase):
    client = Client()
    resp = parse_HTTPResponse(
        client.create(
            data=item
            )
        )
    return BookDB(**resp)


@router.post(
    "/query",
    response_model=List[BookDB]
    )
def query(query: BookQuery):
    client = Client()
    resp = parse_HTTPResponse(
        client.read(
            query=query
            )
        )
    res = [BookDB(**data) for data in resp]
    if len(res) == 0:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
            )
    return res


@router.post(
    "/update/{item_id}",
    response_model=BookDB
    )
def update(query: BookQuery, item_id: str):
    client = Client()
    resp = parse_HTTPResponse(
        client.update(
            item_id=item_id,
            query=query
            )
        )
    return BookDB(**resp)


@router.post(
    "/delete/{item_id}",
    response_model=BookDB
    )
def delete_item(item_id: str):
    client = Client()
    resp = parse_HTTPResponse(
        client.delete(
            item_id=item_id,
            item_type="book"
            )
        )
    return BookDB(**resp)


@router.post(
    "/fulltext",
    response_model=List[BookDB]
    )
def fulltext_search(query: Query):
    client = Client()
    resp = parse_HTTPResponse(
        client.fulltext_search(
            query=query
            )
        )
    return [BookDB(**data) for data in resp]
