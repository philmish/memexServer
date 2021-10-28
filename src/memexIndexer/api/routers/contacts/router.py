from typing import Dict, List
from fastapi import APIRouter, HTTPException
from memexIndexer.api.client import Client
from memexIndexer.api.routers.bookmarks.router import query
from memexIndexer.indexer.schemas import Query
from memexIndexer.utils.http import parse_HTTPResponse
from memexIndexer.api.routers.contacts.schemas import (
    ContactBase,
    ContactDB,
    ContactFulltextQuery,
    ContactQuery,
    DebtBase,
    DebtDB,
    DebtQuery,
    LoanItemBase,
    LoanItemDB,
    LoanItemQuery
)


router = APIRouter(
    prefix="/contact",
    tags=["contact"]
)


@router.get("/ping")
def ping():
    return "Hello World, this is the contacts endpoint"


@router.get(
    "/all",
    response_model=List[ContactDB]
    )
def all_contacts():
    client = Client()
    resp = parse_HTTPResponse(
        client.get_all(
            item_type="contact"
        )
    )
    return [ContactDB(**data) for data in resp]


@router.get(
    "/debt/all",
    response_model=List[DebtDB]
    )
def all_debts():
    client = Client()
    resp = parse_HTTPResponse(
        client.get_all(
            item_type="debt"
        )
    )
    return [DebtDB(**data) for data in resp]


@router.get(
    "/loan_items/all",
    response_model=List[LoanItemDB]
    )
def all_loan_items():
    client = Client()
    resp = parse_HTTPResponse(
        client.get_all(
            item_type="loan_item"
        )
    )
    return [LoanItemDB(**data) for data in resp]

@router.post(
    "/get/id",
    response_model=Dict[str, str]
    )
def get_contact_id(query: ContactQuery):
    client = Client()
    resp = parse_HTTPResponse(
        client.get_id(
            query=query
            )
        )
    return resp


@router.post(
    "/debt/get/id",
    response_model=Dict[str, str]
    )
def get_debt_id(query: DebtQuery):
    client = Client()
    resp = parse_HTTPResponse(
        client.get_id(
            query=query
        )
    )
    return resp


@router.post(
    "/loan_items/get/id",
    response_model=Dict[str, str]
    )
def get_loan_item_id(query: LoanItemQuery):
    client = Client()
    resp = parse_HTTPResponse(
        client.get_id(
            query=query
        )
    )
    return resp



@router.get(
    "/{item_id}",
    response_model=ContactDB
    )
def get_contact_by_id(item_id: str):
    client = Client()
    resp = parse_HTTPResponse(
        client.get_by_id(
            query=Query(
                item_type="contact",
                data=item_id
            )
        )
    )
    return ContactDB(**resp)


@router.get(
    "/debt/{item_id}",
    response_model=DebtDB
    )
def get_debt_by_id(item_id: str):
    client = Client()
    resp = parse_HTTPResponse(
        client.get_by_id(
            query=Query(
                item_type="debt",
                data=item_id
            )
        )
    )
    return DebtDB(**resp)


@router.get(
    "/loan_items/{item_id}",
    response_model=LoanItemDB
    )
def get_loan_item_by_id(item_id: str):
    client = Client()
    resp = parse_HTTPResponse(
        client.get_by_id(
            query=Query(
                item_type="loan_item",
                data=item_id
            )
        )
    )
    return LoanItemDB(**resp)


@router.post(
    "/create",
    response_model=ContactDB
    )
def create_contact(item: ContactBase):
    client = Client()
    resp = parse_HTTPResponse(
        client.create(
            data=item
        )
    )
    return ContactDB(**resp)


@router.post(
    "/debt/create",
    response_model=DebtDB
    )
def create_debt(item: DebtBase):
    client = Client()
    existing_contact = parse_HTTPResponse(
        client.read(
            query=ContactQuery(
                query={"name": item.person}
            )
        )
    )
    existing = [ContactDB(**data) for data in existing_contact]
    if len(existing) != 0:
        resp = parse_HTTPResponse(
            client.create(
                data=item
                )
            )
    else:
        new_contact = ContactBase(name=item.person)
        created_contact = parse_HTTPResponse(
            client.create(
                data=new_contact
            )
        )
        resp = parse_HTTPResponse(
            client.create(
                data=item
            )
        )
    return DebtDB(**resp)


@router.post(
    "/loan_items/create",
    response_model=LoanItemDB
    )
def create_debt(item: LoanItemBase):
    client = Client()
    existing_contact = parse_HTTPResponse(
        client.read(
            query=ContactQuery(
                query={"name": item.person}
            )
        )
    )
    existing = [ContactDB(**data) for data in existing_contact]
    if len(existing) != 0:
        resp = parse_HTTPResponse(
            client.create(
                data=item
                )
            )
    else:
        new_contact = ContactBase(name=item.person)
        created_contact = parse_HTTPResponse(
            client.create(
                data=new_contact
            )
        )
        resp = parse_HTTPResponse(
            client.create(
                data=item
            )
        )
    return LoanItemDB(**resp)


@router.post(
    "/query",
    response_model=List[ContactDB]
    )
def query_contacts(query: ContactQuery):
    client = Client()
    resp = parse_HTTPResponse(
        client.read(
            query=query
        )
    )
    res = [ContactDB(**data) for data in resp]
    if len(res) == 0:
        raise HTTPException(
            status_code=404,
            detail="No items found."
            )
    return res


@router.post(
    "/debt/query",
    response_model=List[DebtDB]
    )
def query_debt(query: DebtQuery):
    client = Client()
    resp = parse_HTTPResponse(
        client.read(
            query=query
        )
    )
    res = [DebtDB(**data) for data in resp]
    if len(res) == 0:
        raise HTTPException(
            status_code=404,
            detail="No items found."
            )
    return res


@router.post(
    "/loan_items/query",
    response_model=List[LoanItemDB]
    )
def query_loan_items(query: LoanItemQuery):
    client = Client()
    resp = parse_HTTPResponse(
        client.read(
            query=query
        )
    )
    res = [LoanItemDB(**data) for data in resp]
    if len(res) == 0:
        raise HTTPException(
            status_code=404,
            detail="No items found."
            )
    return res


@router.post(
    "/update/{item_id}",
    response_model=ContactDB
    )
def update_contact(query: ContactQuery, item_id: str):
    client = Client()
    resp = parse_HTTPResponse(
        client.update(
            item_id=item_id,
            query=query
        )
    )
    return ContactDB(**resp)


@router.post(
    "/debt/update/{item_id}",
    response_model=DebtDB
    )
def update_debt(query: DebtQuery, item_id: str):
    client = Client()
    resp = parse_HTTPResponse(
        client.update(
            item_id=item_id,
            query=query
        )
    )
    return DebtDB(**resp)


@router.post(
    "/loan_items/update/{item_id}",
    response_model=LoanItemDB
    )
def update_loan_item(query: LoanItemQuery, item_id: str):
    client = Client()
    resp = parse_HTTPResponse(
        client.update(
            item_id=item_id,
            query=query
        )
    )
    return LoanItemDB(**resp)



@router.post(
    "/delete/{item_id}",
    response_model=ContactDB
    )
def delete_item(item_id: str):
    client = Client()
    resp = parse_HTTPResponse(
        client.delete(
            item_id=item_id,
            item_type="contact"
        )
    )
    return ContactDB(**resp)


@router.post(
    "/debt/delete/{item_id}",
    response_model=DebtDB
    )
def delete_debt(item_id: str):
    client = Client()
    resp = parse_HTTPResponse(
        client.delete(
            item_id=item_id,
            item_type="debt"
        )
    )
    return DebtDB(**resp)


@router.post(
    "/loan_items/delete/{item_id}",
    response_model=LoanItemDB
    )
def delete_loan_item(item_id: str):
    client = Client()
    resp = parse_HTTPResponse(
        client.delete(
            item_id=item_id,
            item_type="loan_item"
        )
    )
    return LoanItemDB(**resp)


@router.post(
    "/fulltext",
    response_model=List[ContactDB]
    )
def fulltext_search(query: ContactFulltextQuery):
    client = Client()
    resp = parse_HTTPResponse(
        client.fulltext_search(
            query=query
        )
    )
    return [ContactDB(**data) for data in resp]

