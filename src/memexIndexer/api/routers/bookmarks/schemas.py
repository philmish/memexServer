from memexIndexer.api.schemas import ItemBase, ItemQuery
from memexIndexer.indexer.schemas import BlobToIndex, Query
from typing import Optional


class BookmarkBase(ItemBase):
    """Represents the data for a bookmark."""
    link: str
    topic: str
    notes: Optional[str] = ""
    item_type: str = "bookmark"

    def blob(self) -> BlobToIndex:
        return BlobToIndex(
            item_type="bookmark",
            data=f"{self.topic} {self.notes}"
        )

    @property
    def uid(self):
        return {"link": self.link}


class BookmarkFromDB(BookmarkBase):
    """Represents the data from an entry in the bookmarks database collection."""
    _id: str


class BookmarkQuery(ItemQuery):
    item_type: str = "bookmark"


class BookmarkFulltextQuery(Query):
    item_type: str = "bookmark"


