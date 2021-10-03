from memexIndexer.api.schemas import ItemBase, ItemQuery
from typing import Optional

from memexIndexer.indexer.schemas import BlobToIndex


class MovieBase(ItemBase):
    """Represents data for an entry in the movie database collection, based on data returned from the tmdb API."""
    title: str
    budget: Optional[float] = 0
    imdb_id: Optional[str] = ""
    original_language: Optional[str] = ""
    description: Optional[str] = ""
    poster: Optional[str] = ""
    released: Optional[str] = ""
    revenue: Optional[float] = 0
    runtime: Optional[int] = 0
    status: Optional[str] = "Not owned"
    item_type: str = "movie"

    def blob(self) -> BlobToIndex:
        return BlobToIndex(
            item_type="movie",
            data=f"{self.title} {self.original_language} {self.description}"
        )

    @property
    def uid(self):
        return {"title": self.title, "released": self.released}

class MovieDB(MovieBase):
    _id: int

class MovieQuery(ItemQuery):
    item_type: str = "movie"