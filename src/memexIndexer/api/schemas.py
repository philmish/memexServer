from abc import abstractmethod
from pydantic import BaseModel, validator
from datetime import datetime
from pydantic.fields import Field
from memexIndexer.utils.errors import (
    PydanticValidatorError
    )
from typing import (
    Any,
    Dict,
    List,
    Union,
    Optional
    )


class ItemBase(BaseModel):
    item_type: str
    created_At: datetime = Field(
        default_factory=lambda: datetime.now()
        )
    edited_At: Union[datetime, int] = 0
    tags: Union[List[str], List] = Field(
        default_factory=lambda: []
        )

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
            "scraped_data",
            "todo"
            ]
        if v not in valid:
            raise PydanticValidatorError(
                f"{v} is an invalid item_type"
                )
        return v

    @abstractmethod
    def blob(self):
        """Returns a BlobToIndex which can be passed to the indexer database client."""
        pass

    @property
    @abstractmethod
    def uid(self):
        """Returns the unique identifier as dict containing the name and value of the identifier."""
        pass

    @property
    def db_data(self) -> Dict:
        d = self.dict()
        del d["item_type"]
        return d


class ItemQuery(BaseModel):
    item_type: str
    query: Dict[str, Any]

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
            "scraped_data",
            "todo"
            ]
        if v not in valid:
            raise PydanticValidatorError(f"{v} is an invalid item_type")
        return v


class HTTPResponse(BaseModel):
    data: Any
    status: int
    error: Optional[str] = ""
