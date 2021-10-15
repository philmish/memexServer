import os
from datetime import datetime
from bson.objectid import ObjectId
from pymongo import MongoClient
from memexIndexer.indexer.schemas import Query
from memexIndexer.indexer.schemas import BlobToIndex
from memexIndexer.indexer.utils import get_tokens
from memexIndexer.utils.enums import ClientResponse
from memexIndexer.utils.http import parse_client_response
from memexIndexer.api.schemas import (
    HTTPResponse,
    ItemBase,
    ItemQuery
)
try:
    mode = os.getenv("SERVER_MODE")
    if mode == "DEBUG":
        from memexIndexer.config.api_env import default_settings as settings
    # TODO Implement configs for hosting an env from files
    else:
        from memexIndexer.config.api_env import default_settings as settings
except Exception as e:
    # TODO Implement Exception for this case
    raise Exception(f"{e}\nCould not load environment.")


class Client:
    """Database client implementing basic CRUD functionality"""
    def __init__(
        self,
        settings = settings
    ) -> None:
        self.settings = settings
        self.client = MongoClient(
            self.settings.db_host,
            self.settings.db_port
            )
        self.db = self.client.memex_data
        self.indexer_db = self.client.memex_indexes

    def _get_index(self, name: str):
        return self.db[name]

    def _get_indexer(self, name: str):
        return self.indexer_db[name]

    def create(self, data: ItemBase) -> HTTPResponse:
        index = self._get_index(data.item_type)
        exists = index.find_one(data.uid)
        blob = data.blob()

        if exists is not None:
            return parse_client_response(
               response=ClientResponse.EXISTS,
               data=exists
               )

        try:
            new = index.insert_one(data.db_data)
            new_item = index.find_one(new.inserted_id)
            new_item["_id"] = str(new.inserted_id)
            if blob:
                self.index_blob(
                    blob=blob,
                    item_id=str(new.inserted_id)
                    )
            return parse_client_response(
                data=new_item,
                response=ClientResponse.SUCCESS,
                )
        except Exception as e:
            return parse_client_response(
                response=ClientResponse.INTERNALERROR,
                data=e
            )

    def read(self, query: ItemQuery) -> HTTPResponse:
        index = self._get_index(query.item_type)
        results = index.find(query.query)
        if results:
            return parse_client_response(
                response=ClientResponse.SUCCESS,
                data=results
            )
        else:
            return parse_client_response(
                response=ClientResponse.NOTFOUND,
                data=[]
            )

    def update(
        self,
        item_id: str,
        query: ItemQuery
        ) -> HTTPResponse:
        index = self._get_index(query.item_type)
        parsed_item_id = ObjectId(item_id)
        data = query.query
        data["edited_At"] = datetime.now()
        item = index.find_one_and_update(
            {"_id": parsed_item_id},
            {"$set": data}, upsert=True
            )

        if item:
            updated = index.find_one(
                {"_id": parsed_item_id}
                )
            blob_str = ""
            for _, val in data.items():
                if type(val) == str:
                    blob_str += val
            blob = BlobToIndex(
                item_type=query.item_type,
                data=blob_str
            )
            self.index_blob(blob=blob, item_id=item_id)
            return parse_client_response(
                response=ClientResponse.SUCCESS,
                data=updated
            )
        else:
            return parse_client_response(
                response=ClientResponse.NOTFOUND,
                data=None,
                error=f"Id {item_id} could not be found."
            )

    def delete(
        self,
        item_id: str,
        item_type: str
        ) -> HTTPResponse:
        index = self._get_index(item_type)
        parsed_item_id = ObjectId(item_id)
        item = index.find_one_and_delete(
            {"_id": parsed_item_id}
            )
        if item:
            indexer = self._get_indexer(item_type)
            indexer.update_many(
                {"items": item_id},
                {"$pull": {
                    "items": item_id
                    }
                }
            )
            return parse_client_response(
                response=ClientResponse.SUCCESS,
                data=item
            )
        else:
            return parse_client_response(
                response=ClientResponse.NOTFOUND,
                data=None,
                error=f"Id {item_id} could not be found."
            )

    def get_all(self, item_type: str) -> HTTPResponse:
        try:
            index = self._get_index(item_type)
            data = index.find()
            return parse_client_response(
                response=ClientResponse.SUCCESS,
                data=data
            )
        except Exception as e:
            return parse_client_response(
                response=ClientResponse.INTERNALERROR,
                data=[],
                error=f"Could load data for {item_type}\n{e}"
            )


    def get_id(self, query: ItemQuery) -> HTTPResponse:
        index = self._get_index(query.item_type)
        results = index.find_one(query.query)
        if results:
            data = {"id": str(results["_id"])}
            return parse_client_response(
                response=ClientResponse.SUCCESS,
                data=data
            )
        else:
            return parse_client_response(
                response=ClientResponse.NOTFOUND,
                data={"id": ""}
            )

    def get_by_id(self, query: Query):
        index = self._get_index(query.item_type)
        try:
            _id = ObjectId(query.data)
            res = index.find_one({"_id": _id})
            if res:
                return parse_client_response(
                    response=ClientResponse.SUCCESS,
                    data=res
                )
            else:
                return parse_client_response(
                    response=ClientResponse.NOTFOUND,
                    data=[]
                )
        except Exception as e:
            return parse_client_response(
                response=ClientResponse.INTERNALERROR,
                data=e
            )

    def fulltext_search(
        self,
        query: Query
        ) -> HTTPResponse:
        try:
            indexer = self._get_indexer(query.item_type)
            words = get_tokens(query.data)
            results = []
            indexes = indexer.find({"word": {"$in": words}})
            item_index = self._get_index(query.item_type)
            for result in indexes:
                items = result["items"]
                for item in items:
                    data = item_index.find_one(
                        {"_id": ObjectId(item)}
                        )
                    results.append(data)
            return parse_client_response(
                response=ClientResponse.SUCCESS,
                data=results
            )
        except Exception as e:
            return parse_client_response(
                response=ClientResponse.INTERNALERROR,
                data=e
            )

    def index_blob(
        self,
        blob: BlobToIndex,
        item_id: str
        ) -> None:
        index = self._get_indexer(blob.item_type)
        tokens = get_tokens(blob.data)
        for word in tokens:
            exists = index.find_one({"word": word})
            
            if exists and item_id in exists["items"]:
                continue
            elif exists:
                index.find_one_and_update(
                    {"word": word},
                    {"$addToSet": {"items": item_id}}
                    )
            else:
                index.insert_one(
                    {"word": word, "items": [item_id]}
                    )
