from typing import Optional
import os
import logging
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import certifi
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME") or "cricket_db"
COLLECTION_NAME = os.getenv("COLLECTION_NAME") or "matches"


def get_client(timeout_ms: int = 5000) -> Optional[MongoClient]:
	if not MONGO_URI:
		return None
	try:
		connect_kwargs = dict(
			serverSelectionTimeoutMS=timeout_ms,
			connectTimeoutMS=int(os.getenv("MONGO_CONNECT_TIMEOUT_MS") or 10000),
			socketTimeoutMS=int(os.getenv("MONGO_SOCKET_TIMEOUT_MS") or 20000),
			tls=True,
			tlsCAFile=certifi.where(),
		)
		client = MongoClient(MONGO_URI, **connect_kwargs)
		client.admin.command("ping")
		return client
	except PyMongoError as e:
		logging.warning(f"MongoDB connect failed: {e}")
		return None
	except Exception as e:
		logging.warning(f"MongoDB connection error (missing deps or certs?): {e}")
		return None


def get_collection():
	client = get_client()
	if not client:
		raise RuntimeError("MongoDB not available")
	db = client[DATABASE_NAME]
	return db[COLLECTION_NAME]
