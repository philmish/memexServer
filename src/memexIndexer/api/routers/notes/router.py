from typing import List, Dict
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from memexIndexer.api.client import Client
from memexIndexer.indexer.schemas import Query
from memexIndexer.utils.http import parse_HTTPResponse
from memexIndexer.api.routers.notes.schemas import (
    NoteBase,
    NoteDB,
    NoteQuery
)


router = APIRouter(
    prefix="/notes",
    tags=["notes"]
)


@router.get("/ping")
def ping():
    return "Hello World, this is the notes endpoint."


@router.get(
    "/all",
    response_model=List[NoteDB]
    )
def all_notes():
    client = Client()
    resp = parse_HTTPResponse(
        client.get_all(
            item_type="notes"
            )
        )
    return [NoteDB(**data) for data in resp]


@router.post(
    "/get/id",
    response_model=Dict[str, str]
    )
def get_id(query: NoteQuery):
    client = Client()
    resp = parse_HTTPResponse(
        client.get_id(
            query=query
            )
        )
    return resp


@router.post(
    "/create",
    response_model=NoteDB
    )
def create_note(item: NoteBase):
    client = Client()
    resp = parse_HTTPResponse(
        client.create(
            data=item
            )
        )
    return NoteDB(**resp)


@router.post(
    "/query",
    response_model=List[NoteDB]
    )
def query(query: NoteQuery):
    client = Client()
    resp = parse_HTTPResponse(
        client.read(
            query=query
            )
        )
    res = [NoteDB(**data) for data in resp]
    if len(res) == 0:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
            )
    return res
    

@router.post(
    "/update/{item_id}",
    response_model=NoteDB
    )
def update(query: NoteQuery, item_id: str):
    client = Client()
    resp = parse_HTTPResponse(
        client.update(
            item_id=item_id,
            query=query
            )
        )
    return NoteDB(**resp)


@router.post(
    "/delete/{item_id}",
    response_model=NoteDB
    )
def delete_item(item_id: str):
    client = Client()
    resp = parse_HTTPResponse(
        client.delete(
            item_id=item_id,
            item_type="note"
            )
        )
    return NoteDB(**resp)


@router.post(
    "/fulltext",
    response_model=List[NoteDB]
    )
def fulltext_search(query: Query):
    client = Client()
    resp = parse_HTTPResponse(
        client.fulltext_search(
            query=query
            )
        )
    return [NoteDB(**data) for data in resp]
