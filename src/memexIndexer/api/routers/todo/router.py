from typing import List, Dict
from fastapi import APIRouter
from fastapi import HTTPException
from memexIndexer.api.client import Client
from memexIndexer.indexer.schemas import Query
from memexIndexer.utils.http import parse_HTTPResponse
from memexIndexer.api.routers.todo.schemas import (
    ToDoBase,
    TodoDB,
    TodoFulltextQuery,
    TodoQuery
)


router = APIRouter(
    prefix="/todo",
    tags=["todo"]
)


@router.get("/ping")
def ping():
    return "Hello World, this is the todos endpoint."


@router.get(
    "/all",
    response_model=List[TodoDB])
def all_todos():
    client = Client()
    resp = parse_HTTPResponse(
        client.get_all(
            item_type="todo"
        )
    )
    return [TodoDB(**data) for data in resp]


@router.post(
    "/get/id",
    response_model=Dict[str, str]
)
def get_id(query: TodoQuery):
    client = Client()
    resp = parse_HTTPResponse(
        client.get_id(
            query=query
        )
    )
    return resp


@router.get(
    "/{item_id}",
    response_model=TodoDB
    )
def get_by_id(item_id: int):
    client = Client()
    resp = parse_HTTPResponse(
        client.get_by_id(
            query=Query(
                item_type="todo",
                data=item_id
            )
        )
    )
    return TodoDB(**resp)


@router.post(
    "/create",
    response_model=TodoDB
    )
def create_todo(item: ToDoBase):
    client = Client()
    resp = parse_HTTPResponse(
        client.create(
            data=item
        )
    )
    return TodoDB(**resp)


@router.post(
    "/query",
    response_model=List[TodoDB]
    )
def query(query: TodoQuery):
    client = Client()
    resp = parse_HTTPResponse(
        client.read(
            query=query
        )
    )
    res = [TodoDB(**data) for data in resp]
    if len(res) == 0:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )
    return res


@router.post(
    "/update/{item_id}",
    response_model=TodoDB
    )
def update(query: TodoQuery, item_id: str):
    client = Client()
    resp = parse_HTTPResponse(
        client.update(
            item_id=item_id,
            query=query
        )
    )
    return TodoDB(**resp)


@router.post(
    "/delete/{item_id}",
    response_model=TodoDB
    )
def delete_item(item_id: str):
    client = Client()
    resp = parse_HTTPResponse(
        client.delete(
            item_id=item_id,
            item_type="todo"
            )
        )
    return TodoDB(**resp)


@router.post(
    "/fulltext",
    response_model=List[TodoDB]
    )
def fulltext_search(query: TodoFulltextQuery):
    client = Client()
    resp = parse_HTTPResponse(
        client.fulltext_search(
            query=query
            )
        )
    return [TodoDB(**data) for data in resp]
