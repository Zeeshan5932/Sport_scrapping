from typing import Optional, Dict, Any, List
import logging
import asyncio

from config import settings
from .mongo_storage import MongoStorage
from .json_storage import JSONStorage
from dateutil import parser as dateparser
from datetime import datetime


_GLOBAL_MANAGER = None


def set_storage_manager(mgr):
    global _GLOBAL_MANAGER
    _GLOBAL_MANAGER = mgr


def get_storage_manager():
    global _GLOBAL_MANAGER
    if _GLOBAL_MANAGER is None:
        # lazy default manager
        _GLOBAL_MANAGER = StorageManager()
    return _GLOBAL_MANAGER


class StorageManager:
    """High-level storage manager. Tries Mongo, falls back to JSON.

    Methods are synchronous; use from async code via `asyncio.to_thread` if needed.
    """
    def __init__(self, mongo: Optional[MongoStorage] = None, json_store: Optional[JSONStorage] = None) -> None:
        self.mongo = mongo or MongoStorage()
        self.json = json_store or JSONStorage()
        self.sync_interval = int(getattr(settings, "SYNC_INTERVAL", 30) or 30)

    def save_master(self, data: Dict[str, Any]) -> None:
        """Save master document. Try MongoDB first, fallback to JSON and pending."""
        try:
            if self.mongo.is_available():
                self.mongo.save_master(data)
                # also update daily JSON as backup
                try:
                    self.json.save_master(data)
                except Exception:
                    logging.debug("Failed to update daily JSON backup after Mongo save")
                return
        except Exception as e:
            logging.warning(f"Mongo save failed: {e}")
        # Fallback: save JSON backup only (no pending.json usage)
        logging.warning("Mongo save failed; saving local JSON backup only")
        try:
            self.json.save_master(data)
        except Exception as e:
            logging.error(f"Failed to save local JSON: {e}")

    def load_master(self, date: str) -> Optional[Dict[str, Any]]:
        # Try Mongo first
        try:
            if self.mongo.is_available():
                d = self.mongo.load_master(date)
                if d:
                    return d
        except Exception:
            pass

        # Fallback to JSON daily
        try:
            return self.json.load_master(date)
        except Exception:
            return None

    def sync_pending(self) -> None:
        # Scan daily backup files and upload those missing in Mongo
        try:
            if not self.mongo.is_available():
                logging.info("Mongo not available; skipping sync")
                return

            dates = self.json.list_daily_files()
            for date in dates:
                try:
                    # if mongo already has it, skip
                    existing = self.mongo.load_master(date)
                    if existing:
                        continue
                    # load local file and upload
                    local = self.json.load_master(date)
                    if local:
                        self.mongo.save_master(local)
                        logging.info(f"Synced local backup for date {date} to Mongo")
                except Exception as e:
                    logging.warning(f"Failed to sync local file for {date}: {e}")
        except Exception as e:
            logging.warning(f"sync_pending error: {e}")

    def normalize_date(self, date_str: str) -> str:
        """Parse various date formats and return YYYY-MM-DD."""
        try:
            dt = dateparser.parse(date_str)
            return dt.strftime("%Y-%m-%d")
        except Exception:
            # as fallback, return input if it already matches YYYY-MM-DD
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                return date_str
            except Exception:
                raise

    async def sync_loop(self) -> None:
        while True:
            try:
                await asyncio.sleep(self.sync_interval)
                # run sync in thread to avoid blocking
                await asyncio.to_thread(self.sync_pending)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logging.warning(f"Sync loop error: {e}")
