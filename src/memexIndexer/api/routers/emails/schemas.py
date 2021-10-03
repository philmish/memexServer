from datetime import datetime
from typing import List, Optional, Union

from pydantic.fields import Field
from memexIndexer.api.schemas import ItemBase, ItemQuery
from memexIndexer.indexer.schemas import BlobToIndex


class Email(ItemBase):
    recieved_at: Union[str, datetime]
    sender: str
    subject: str
    content: str
    cc: Optional[Union[List[str],List]] = Field(default_factory=lambda: [])
    bcc: Optional[Union[List[str],List]] = Field(default_factory=lambda: [])
    item_type: str = "email"

    def blob(self) -> BlobToIndex:
        return BlobToIndex(
            item_type="email",
            data=f"{self.subject} {self.content}"
        )

    @property
    def uid(self):
        return {
            "sender": self.sender,
            "subject": self.subject,
            "recieved_at": self.recieved_at
            }


class EmailFromDB(Email):
    _id: str


class EmailQuery(ItemQuery):
    item_type: str = "email"