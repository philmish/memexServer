from typing import List, Dict
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from memexIndexer.api.client import Client
from memexIndexer.utils.http import parse_HTTPResponse
from memexIndexer.indexer.schemas import Query
from memexIndexer.api.routers.emails.schemas import (
    Email,
    EmailFromDB,
    EmailQuery
)


router = APIRouter(
    prefix="/email",
    tags=["email"]
)


@router.get("/ping")
def ping():
    return "Hello World, this is the email endpoint."


@router.get(
    "/all",
    response_model=List[EmailFromDB]
    )
def all_emails():
    client = Client()
    resp = parse_HTTPResponse(
        client.get_all(
            item_type="email"
            )
        )
    return [EmailFromDB(**data) for data in resp]


@router.post(
    "/get/id",
    response_model=Dict[str, str]
    )
def get_id(query: EmailQuery):
    client = Client()
    resp = parse_HTTPResponse(
        client.get_id(
            query=query
            )
        )
    return resp


@router.post(
    "/create",
    response_model=EmailFromDB
    )
def create_email(item: Email):
    client = Client()
    resp = parse_HTTPResponse(
        client.create(
            data=item
            )
        )
    return EmailFromDB(**resp)


@router.post(
    "/query",
    response_model=List[EmailFromDB]
    )
def query(query: EmailQuery):
    client = Client()
    resp = parse_HTTPResponse(
        client.read(
            query=query
            )
        )
    res = [EmailFromDB(**data) for data in resp]
    if len(res) == 0:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
            )
    return res


@router.post(
    "/update/{item_id}",
    response_model=EmailFromDB
    )
def update(query: EmailQuery, item_id: str):
    client = Client()
    resp = parse_HTTPResponse(
        client.update(
            item_id=item_id,
            query=query
            )
        )
    return EmailFromDB(**resp)


@router.post(
    "/delete/{item_id}",
    response_model=EmailFromDB
    )
def delete_item(item_id: str):
    client = Client()
    resp = parse_HTTPResponse(
        client.delete(
            item_id=item_id,
            item_type="email"
            )
        )
    return EmailFromDB(**resp)


@router.post(
    "/fulltext",
    response_model=List[EmailFromDB]
    )
def fulltext_search(query: Query):
    client = Client()
    resp = parse_HTTPResponse(
        client.fulltext_search(
            query=query
            )
        )
    return [EmailFromDB(**data) for data in resp]
