import os

DEFAULT_MONGO_URI = "mongodb+srv://IRGC:iraniraniran@iranmaldb.gurutam.mongodb.net/"
DEFAULT_DB_NAME = "IranMalDB"
DEFAULT_COLLECTION = "tweets"
DEFAULT_WEAPONS_FILE = "/app/data/weapons.txt"

MONGO_URI = os.getenv("MONGO_URI", DEFAULT_MONGO_URI)
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", DEFAULT_DB_NAME)
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", DEFAULT_COLLECTION)
WEAPONS_FILE = os.getenv("WEAPONS_FILE", DEFAULT_WEAPONS_FILE)
