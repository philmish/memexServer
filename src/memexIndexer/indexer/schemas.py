from pydantic import BaseModel, validator
from typing import Any, List, Union
from memexIndexer.utils.errors import PydanticValidatorError


class Request(BaseModel):
    """Represents a basic text blob used to transfer data from and to the Indexer"""
    item_type: str

    @validator("item_type")
    def valid_item_type_check(cls, v):
        v = v.lower()
        valid = [
            "bookmark",
            "email",
            "contact",
            "book",
            "movie",
            "note",
            "time_capsule",
            "scraped_data"
            "tag"
            ]
        if v not in valid:
            raise PydanticValidatorError(f"{v} is an invalid item_type")
        return v


class IndexedBlob(Request):
    """Represents a blob of text which is added to the index of its item_type"""
    item_id: str
    data: str


class BlobToIndex(Request):
    data: str


class Query(Request):
    """Represents a query send to the Indexer"""
    data: str


class DeleteRequest(Request):
    """Represents a delete action for an item, which means the correlated ID must be delted from the index."""
    item_id: str


class Response(BaseModel):
    """Represents the Response from the Indexer to any kind of request"""
    results: List[Any]
    error: Union[str, None] = None


class DBEntry(BaseModel):
    """Represents an entry in an index"""
    id: str
    word: str
    items: List[str]