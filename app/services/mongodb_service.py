
from pymongo import MongoClient
from pymongo.database import Database


class MongoDBService:
    """Manages MongoDB database connections."""

    DATABASE_NAME = "ai_study_assistant"

    def __init__(self, uri: str = "mongodb://localhost:27017"):
        self.client = MongoClient(uri)
        self.database: Database = self.client[self.DATABASE_NAME]

    def test_connection(self) -> bool:
        """Check whether MongoDB is connected."""

        self.client.admin.command("ping")

        print("MongoDB connected successfully.")

        return True

    def get_collection(self, collection_name: str):
        """Get a MongoDB collection."""

        return self.database[collection_name]

    def close(self) -> None:
        """Close the MongoDB connection."""

        self.client.close()
