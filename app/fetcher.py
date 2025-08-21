from typing import List, Dict
import os
from pymongo import MongoClient
import pandas as pd


class MongoFetcher:
    def __init__(self):
        self.mongo_uri = os.getenv("mongodb+srv://IRGC:iraniraniran@iranmaldb.gurutam.mongodb.net/")
        if not self.mongo_uri:
            raise ValueError("Missing environment variable MONGO_URI")

        self.db_name = os.getenv("MONGO_DB_NAME", "IranMalDB")
        self.collection_name = os.getenv("MONGO_COLLECTION", "tweets")

        self.client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=5000)
        self.client.admin.command("ping")
        self.collection = self.client[self.db_name][self.collection_name]

    def fetch_all(self) -> pd.DataFrame:
        docs: List[Dict] = list(self.collection.find({}, {"_id": 1, "text": 1}))
        records = []
        for d in docs:
            _id = str(d.get("_id"))
            text = d.get("text", "")
            records.append({"id": _id, "original_text": text})
        return pd.DataFrame(records)
