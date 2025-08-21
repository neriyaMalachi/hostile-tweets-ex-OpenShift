from typing import List, Dict
import os
from pymongo import MongoClient
import pandas as pd
from .config import MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION  # ← חדש



class MongoFetcher:

    def __init__(self):
        self.mongo_uri = MONGO_URI
        self.db_name = MONGO_DB_NAME
        self.collection_name = MONGO_COLLECTION

        self.client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=5000)
        self.client.admin.command("ping")
        self.collection = self.client[self.db_name][self.collection_name]

    def fetch_all(self) -> pd.DataFrame:
        docs: List[Dict] = list(self.collection.find({}, {"TweetID": 1, "Text": 1}))
        records = []
        for d in docs:
            _id = str(d.get("_id"))
            text = d.get("Text", "")
            records.append({"id": _id, "original_text": text})
        return pd.DataFrame(records)
