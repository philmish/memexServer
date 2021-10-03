from typing import List, Dict
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from memexIndexer.api.client import Client
from memexIndexer.api.routers.movies.schemas import (
    MovieBase,
    MovieDB,
    MovieQuery
)
from memexIndexer.indexer.schemas import Query
from memexIndexer.utils.http import parse_HTTPResponse


router = APIRouter(
    prefix="/movies",
    tags=["movies"]
)


@router.get("/ping")
def ping():
    return "Hello World, this is the moviess endpoint."


@router.get(
    "/all",
    response_model=List[MovieDB]
    )
def all_notes():
    client = Client()
    resp = parse_HTTPResponse(
        client.get_all(
            item_type="movies"
            )
        )
    return [MovieDB(**data) for data in resp]


@router.post(
    "/get/id",
    response_model=Dict[str, str]
    )
def get_id(query: MovieQuery):
    client = Client()
    resp = parse_HTTPResponse(
        client.get_id(
            query=query
            )
        )
    return resp


@router.post(
    "/create",
    response_model=MovieDB
    )
def create_movie(item: MovieBase):
    client = Client()
    resp = parse_HTTPResponse(
        client.create(
            data=item
            )
        )
    return MovieDB(**resp)


@router.post(
    "/query",
    response_model=List[MovieDB]
    )
def query(query: MovieQuery):
    client = Client()
    resp = parse_HTTPResponse(
        client.read(
            query=query
            )
        )
    res = [MovieDB(**data) for data in resp]
    if len(res) == 0:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
            )
    return res
    

@router.post(
    "/update/{item_id}",
    response_model=MovieDB
    )
def update(query: MovieQuery, item_id: str):
    client = Client()
    resp = parse_HTTPResponse(
        client.update(
            item_id=item_id,
            query=query
            )
        )
    return MovieDB(**resp)


@router.post(
    "/delete/{item_id}",
    response_model=MovieDB
    )
def delete_item(item_id: str):
    client = Client()
    resp = parse_HTTPResponse(
        client.delete(
            item_id=item_id,
            item_type="movie"
            )
        )
    return MovieDB(**resp)


@router.post(
    "/fulltext",
    response_model=List[MovieDB]
    )
def fulltext_search(query: Query):
    client = Client()
    resp = parse_HTTPResponse(
        client.fulltext_search(
            query=query
            )
        )
    return [MovieDB(**data) for data in resp]


