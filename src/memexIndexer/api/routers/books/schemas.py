from typing import Optional
from memexIndexer.api.schemas import ItemBase, ItemQuery
from memexIndexer.indexer.schemas import BlobToIndex


class BookBase(ItemBase):
    """Represents basic data for a book."""
    title: str
    author: str
    isbn: str
    pages: Optional[int] = 0
    item_type: str = "book"
    
    def blob(self):
        return BlobToIndex(
            item_type="book",
            data=f"{self.author} {self.title}"
        )

    @property
    def uid(self):
        return {"isbn": self.isbn}


class BookDB(BookBase):
    """Represents data for a book from an database entry."""
    _id: int


class BookQuery(ItemQuery):
    item_type: str = "book"