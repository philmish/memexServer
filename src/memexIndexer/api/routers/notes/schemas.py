from memexIndexer.api.schemas import ItemBase, ItemQuery
from memexIndexer.indexer.schemas import BlobToIndex

class NoteBase(ItemBase):
    text: str
    item_type: str = "note"

    def blob(self) -> BlobToIndex:
        return BlobToIndex(
            item_type="note",
            data=self.text
        )

    @property
    def uid(self):
        return {"created_At": self.created_At, "text": self.text}


class NoteDB(NoteBase):
    _id: int


class NoteQuery(ItemQuery):
    item_type: str = "note"