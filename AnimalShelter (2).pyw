# AnimalShelter.py
from pymongo import MongoClient


class AnimalShelter:
    """
    CRUD operations for the AAC MongoDB collection
    """

    def __init__(
        self,
        username: "aacuser",
        password: "ChangeMe123",
        host: str = "127.0.0.1",
        port: int = 27017,
        db_name: str = "aac",
        collection_name: str = "animals",
        auth_source: str = "admin",
    ):
        """
        Initialize MongoDB connection.

        NOTE: In the SNHU CS-340 environment, the user is commonly created in the
        'admin' database, so authSource must be 'admin' even if you are using the 'aac' DB.
        """
        try:
            uri = f"mongodb://{username}:{password}@{host}:{port}/?authSource={auth_source}"
            self.client = MongoClient(uri)

            # Force a connection/auth check immediately (so errors show here)
            self.client.admin.command("ping")

            self.database = self.client[db_name]
            self.collection = self.database[collection_name]
            print("MongoDB connected successfully!")
        except Exception as e:
            print("MongoDB connection failed:", e)
            raise  # re-raise so you see the real error and stop execution

    def create(self, data: dict):
        """Insert a new document"""
        if not data or not isinstance(data, dict):
            raise ValueError("Data must be a non-empty dictionary.")
        return self.collection.insert_one(data).inserted_id

    def read(self, query: dict = None):
        """Read documents from the collection"""
        if query is None:
            query = {}
        return list(self.collection.find(query))

    def update(self, query: dict, update_values: dict):
        """Update documents matching the query"""
        if not query or not update_values:
            raise ValueError("Query and update values required.")
        result = self.collection.update_many(query, {"$set": update_values})
        return result.modified_count

    def delete(self, query: dict):
        """Delete documents matching the query"""
        if not query:
            raise ValueError("Query required.")
        result = self.collection.delete_many(query)
        return result.deleted_count
