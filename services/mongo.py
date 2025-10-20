from pymongo import MongoClient

class MongoService:
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def upload_document(self, collection_name: str, document: dict):
        collection = self.db[collection_name]
        result = collection.insert_one(document)
        if result.inserted_id is None:
            raise

if __name__ == "__main__":
    mongo = MongoService("mongodb://fintree_scraper:QuV0Xr1McMVca9VQGdip7KVJ6RyI0xFaL9p63BJWrT4%3D@localhost:27017/?authSource=fintree", "fintree")
    mongo.upload_document("falabella", {"caca": "peo"})