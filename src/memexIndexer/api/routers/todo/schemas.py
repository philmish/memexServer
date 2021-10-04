from datetime import datetime
from memexIndexer.api.schemas import ItemBase, ItemQuery
from memexIndexer.indexer.schemas import BlobToIndex, Query
from typing import Optional, Union


class ToDoBase(ItemBase):
    """Represents the data for a to do."""
    description: str
    importance: int = 1
    due_date: Optional[datetime] = 0
    item_type: str = "todo"

    def blob(self):
        """Returns data from all relevant text fields for tokenizing and fulltext indexing."""
        return BlobToIndex(
            item_type="todo",
            data=self.description
        )

    @property
    def uid(self):
        """The uid property returns a query string for the data bank client, which is used to ensure item uniquenes."""
        return {
            "description": self.description,
            "created_At": self.created_At
            }


class TodoDB(ToDoBase):
    _id: str


class TodoQuery(ItemQuery):
    """Represents a query. Sets the item_type parameter per default."""
    item_type: str = "todo"


class TodoFulltextQuery(Query):
    """Represents a query for a fulltext query to the endpoint. Sets item_type per default."""
    item_type: str = "todo"