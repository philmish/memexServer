from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from memexIndexer.api.client import Client
from memexIndexer.indexer.schemas import Query
from memexIndexer.api.schemas import (
    HTTPResponse,
    ItemQuery,
    ItemBase
)

# TODO Needs reimplementation for endpoints to query for debt and loan items.
router = APIRouter(
    prefix="/contact",
    tags=["contact"]
)


@router.get("/all", response_model=HTTPResponse)
def all_notes():
    client = Client()
    resp = client.get_all(item_type="contact")
    return JSONResponse(content=jsonable_encoder(resp))


@router.post("/create", response_model=HTTPResponse)
def create_note(item: ItemBase):
    client = Client()
    resp = client.create(data=item)
    return JSONResponse(content=jsonable_encoder(resp))


@router.post("/query", response_model=HTTPResponse)
def query(query: ItemQuery):
    client = Client()
    resp = client.read(query=query)
    return JSONResponse(content=jsonable_encoder(resp))
    

@router.post("/update/{item_id}", response_model=HTTPResponse)
def update(query: ItemQuery, item_id: str):
    client = Client()
    resp = client.update(item_id=item_id)
    return JSONResponse(content=jsonable_encoder(resp))


@router.post("/delete/{item_id}", response_model=HTTPResponse)
def delete_item(item_id: str):
    client = Client()
    resp = client.delete(item_id=item_id)
    return JSONResponse(content=jsonable_encoder(resp))

@router.post("/bytags", response_class=HTTPResponse)
def get_by_tags():
    # TODO Implement endpoint.
    pass


@router.post("/fulltext", response_model=HTTPResponse)
def fulltext_search(query: Query):
    client = Client()
    resp = client.fulltext_search(query=query)
    return JSONResponse(content=jsonable_encoder(resp))

