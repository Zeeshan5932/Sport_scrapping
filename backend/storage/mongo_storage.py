from typing import Optional, Any, Dict
import logging
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import os
import certifi

from config import settings


class MongoStorage:
    def __init__(self, uri: Optional[str] = None, database: Optional[str] = None, collection: str = "matches") -> None:
        self.uri = uri or settings.MONGO_URI
        self.database_name = database or os.getenv("DATABASE_NAME") or "cricket_db"
        self.collection_name = collection or os.getenv("COLLECTION_NAME") or "matches"
        self.client: Optional[MongoClient] = None
        self._connect()

    def _connect(self) -> None:
        if not self.uri:
            logging.info("Mongo URI not configured; MongoStorage disabled.")
            return
        try:
            # Use certifi CA bundle for TLS verification with Atlas
            connect_kwargs = dict(
                serverSelectionTimeoutMS=int(os.getenv("MONGO_SERVER_SELECTION_TIMEOUT_MS") or 10000),
                connectTimeoutMS=int(os.getenv("MONGO_CONNECT_TIMEOUT_MS") or 10000),
                socketTimeoutMS=int(os.getenv("MONGO_SOCKET_TIMEOUT_MS") or 20000),
            )

            # Decide whether to enable TLS based on URI or explicit env var.
            mongo_tls = os.getenv("MONGO_TLS")
            use_tls = False
            if self.uri.startswith("mongodb+srv://"):
                use_tls = True
            elif mongo_tls and mongo_tls.lower() in ("1", "true", "yes"):
                use_tls = True

            if use_tls:
                # Use certifi CA bundle for TLS verification with Atlas or explicit TLS
                connect_kwargs.update({
                    "tls": True,
                    "tlsCAFile": certifi.where(),
                })

            self.client = MongoClient(self.uri, **connect_kwargs)
            # quick check
            self.client.admin.command("ping")
            logging.info("MongoDB connected")
        except Exception as e:
            # Catch all to ensure missing certifi/dnspython or TLS issues are logged
            logging.warning(f"Mongo connection failed: {e}")
            self.client = None

    def is_available(self) -> bool:
        if not self.client:
            return False
        try:
            self.client.admin.command("ping")
            return True
        except PyMongoError:
            return False

    def _col(self):
        if not self.client:
            raise RuntimeError("Mongo client not available")
        return self.client[self.database_name][self.collection_name]

    def save_master(self, data: Dict[str, Any]) -> None:
        try:
            col = self._col()
            col.replace_one({"date": data["date"]}, data, upsert=True)
        except Exception as e:
            raise

    def load_master(self, date: str) -> Optional[Dict[str, Any]]:
        try:
            col = self._col()
            doc = col.find_one({"date": date}, {"_id": 0})
            return doc
        except Exception:
            return None

    def sync_docs(self, docs: list) -> list:
        # Attempt to save multiple docs. Return list of successfully synced dates
        synced = []
        for d in docs:
            try:
                self.save_master(d)
                synced.append(d.get("date"))
            except Exception as e:
                logging.warning(f"Failed to sync doc {d.get('date')}: {e}")
        return synced
