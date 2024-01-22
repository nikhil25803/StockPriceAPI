# Imports
import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from fastapi import HTTPException, status

# Take environment variables from .env.
load_dotenv()

# Get the Mongo DB URL from .env file
MONGO_URI = os.environ.get("MONGO_URI")

# Create a new client and connect to the server
client = MongoClient(MONGO_URI, server_api=ServerApi("1"))


def connect_db(DB_URI: str = MONGO_URI):
    # Test the connection
    try:
        client.admin.command("ping")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to connect to database",
        )
