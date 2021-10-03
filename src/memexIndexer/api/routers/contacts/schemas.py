from pydantic import Field
from typing import Optional, List
from memexIndexer.api.schemas import ItemBase
from memexIndexer.indexer.schemas import BlobToIndex


class DebtBase(ItemBase):
    """Represents data for entry in the debt database collection."""
    person: str
    value: float
    owed_to_me: Optional[bool] = True

    def blob(self):
        pass


class DebtDB(DebtBase):
    """Represents data from entry in the debt database collection."""
    _id: str


class LoanItemBase(ItemBase):
    """Represents the data for a entry in the loan items database collection."""
    person: str
    item: str
    loan_from_me: Optional[bool] = True

    def blob(self):
        pass


class LoanItemDB(LoanItemBase):
    """Represents the data from a entry in the loan items database collection."""
    _id: str


class ContactBase(ItemBase):
    """Represents a contact which can be linked to debts and loan items."""
    name: str
    birthday: Optional[str] = ""
    address: Optional[str] = ""
    e_mail: Optional[str] = ""
    telephone: Optional[str] = ""
    notes: Optional[str] = ""
    loan_items: List[LoanItemBase] = Field(default=lambda: [])
    debts: List[DebtBase] = Field(default=lambda: [])

    def blob(self) -> BlobToIndex:
        return BlobToIndex(
            item_type="contact",
            data=self.notes
        )


class ContactDB(ContactBase):
    """Represents data from an entry in the contact database collection."""
    _id: str
