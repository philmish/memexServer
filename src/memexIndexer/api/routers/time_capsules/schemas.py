from memexIndexer.api.schemas import ItemBase, ItemQuery


class TimeCapsuleBase(ItemBase):
    link: str
    archive: str
    item_type: str = "time_capsule"

    def blob(self):
        pass

    @property
    def uid(self):
        return {"archive": self.archive}


class TimeCapsuleDB(TimeCapsuleBase):
    _id: int


class TimeCapsuleQuery(ItemQuery):
    item_type: str = "time_capsule"
