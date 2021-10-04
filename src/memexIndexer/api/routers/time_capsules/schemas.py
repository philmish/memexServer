from memexIndexer.api.schemas import ItemBase, ItemQuery
from datetime import datetime

class TimeCapsuleBase(ItemBase):
    link: str
    archive: str
    item_type: str = "time_capsule"
    timestamp: datetime

    def blob(self):
        pass

    @property
    def uid(self):
        return {
            "link": self.link,
            "timestamp": self.timestamp
            }


class TimeCapsuleDB(TimeCapsuleBase):
    _id: int


class TimeCapsuleQuery(ItemQuery):
    item_type: str = "time_capsule"
