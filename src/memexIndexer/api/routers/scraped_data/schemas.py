from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, validator
from pydantic.fields import Field
from memexIndexer.api.schemas import ItemBase
from memexIndexer.indexer.schemas import BlobToIndex
from memexIndexer.utils.errors import PydanticValidatorError


class ScrapeRequest(BaseModel):
    plugin: str
    slug: str
    method: str = "GET"
    header: Optional[Dict[str,Any]]

    @validator("method")
    def validate_method(cls, v):
        methods = ["GET", "POST", "PUT", "DELETE"]
        if v not in methods:
            raise PydanticValidatorError(
                f"{v} is not a valid HTTP method"
            )

class ScrapedDataBase(ItemBase):
    """Represents the base for all schemas for data scraped from the web."""
    link: str
    status_code: int
    response_header: Dict[str,Any]
    timestamp: Optional[datetime] = Field(
        default_factory=lambda: datetime.now()
        )
    data: Any
    item_type: str = "scraped_data"

    def blob(self):
        return str(self.data)

    @property
    def uid(self):
        return {"created_At": self.created_At, "link": self.link}

class ScrapedDataDB(ScrapedDataBase):
    _id: str