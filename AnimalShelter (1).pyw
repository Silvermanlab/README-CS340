# AnimalShelter.py
from pymongo import MongoClient

class AnimalShelter:
    """
    CRUD operations for the AAC MongoDB collection
    """

    def __init__(self, username, password, host="localhost", port=27017, db_name="aac"):
        """
        Initialize MongoDB connection
        """
        try:
            self.client = MongoClient(
                f"mongodb://{username}:{password}@{host}:{port}/{db_name}?authSource=admin"
            )
            self.database = self.client[db_name]
            self.collection = self.database["animals"]
            print("MongoDB connected successfully!")
        except Exception as e:
            print("MongoDB connection failed:", e)

    def create(self, data: dict):
        """Insert a new document"""
        if data:
            return self.collection.insert_one(data).inserted_id
        else:
            raise ValueError("Data must be a non-empty dictionary.")

    def read(self, query: dict = {}):
        """Read documents from the collection"""
        try:
            return list(self.collection.find(query))
        except Exception as e:
            print("Read failed:", e)
            return []

    def update(self, query: dict, update_values: dict):
        """Update documents matching the query"""
        if query and update_values:
            return self.collection.update_many(query, {"$set": update_values}).modified_count
        else:
            raise ValueError("Query and update values required.")

    def delete(self, query: dict):
        """Delete documents matching the query"""
        if query:
            return self.collection.delete_many(query).deleted_count
        else:
            raise ValueError("Query required.")
