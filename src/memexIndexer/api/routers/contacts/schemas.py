from pydantic import Field
from typing import Optional, List
from memexIndexer.api.schemas import ItemBase, ItemQuery
from memexIndexer.indexer.schemas import BlobToIndex, Query


class DebtBase(ItemBase):
    """Represents data for entry in the debt database collection."""
    person: str
    value: float
    owed_to_me: Optional[bool] = True
    item_type: str = "debt"

    def blob(self):
        pass

    @property
    def uid(self):
        return {
            "created_At": self.created_At,
            "person": self.person,
            "value": self.value
            }


class DebtDB(DebtBase):
    """Represents data from entry in the debt database collection."""
    _id: str


class DebtQuery(ItemQuery):
    item_type: str = "debt"


class LoanItemBase(ItemBase):
    """Represents the data for a entry in the loan items database collection."""
    person: str
    item: str
    loan_from_me: Optional[bool] = True
    item_type: str = "loan_item"

    def blob(self):
        pass

    @property
    def uid(self):
        return {
            "created_At": self.created_At,
            "person": self.person,
            "item": self.item
            }


class LoanItemDB(LoanItemBase):
    """Represents the data from a entry in the loan items database collection."""
    _id: str


class LoanItemQuery(ItemQuery):
    item_type: str = "loan_item"


class ContactBase(ItemBase):
    """Represents a contact which can be linked to debts and loan items."""
    name: str
    birthday: Optional[str] = ""
    address: Optional[str] = ""
    e_mail: Optional[str] = ""
    telephone: Optional[str] = ""
    notes: Optional[str] = ""
    loan_items: List[str] = Field(default_factory=lambda: [])
    debts: List[str] = Field(default_factory=lambda: [])
    item_type: str = "contact"

    def blob(self) -> BlobToIndex:
        return BlobToIndex(
            item_type="contact",
            data=self.notes
        )

    @property
    def uid(self):
        return {
            "name": self.name,
            "birthday": self.birthday,
            }


class ContactDB(ContactBase):
    """Represents data from an entry in the contact database collection."""
    _id: str


class ContactQuery(ItemQuery):
    item_type: str = "contact"


class ContactFulltextQuery(Query):
    item_type: str = "contact"
