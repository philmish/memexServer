from typing import Optional
from memexIndexer.api.schemas import ItemBase
from memexIndexer.indexer.schemas import BlobToIndex

class ScrapedDataBase(ItemBase):
    """Represents the base for all schemas for data scraped from the web."""
    link: str
    item_type: str = "scraped_data"

    def blob(self):
        pass

    @property
    def uid(self):
        return {"created_At": self.created_At, "link": self.link}

class ScrapedArticle(ScrapedDataBase):
    """Represents a data from a scraped article."""
    title: str
    content: str
    author: Optional[str] = ""

    def blob(self) -> BlobToIndex:
        return BlobToIndex(
            item_type=self.item_type,
            data=f"{self.title} {self.content} {self.author}"
        )


class ScrapedArticleDB(ScrapedArticle):
    _id: str