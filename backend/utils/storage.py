import os
from datetime import datetime
from typing import Optional, Dict, Any
import logging

from config import settings
from storage.storage_manager import get_storage_manager


def get_output_path():
    today = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(settings.DATA_FOLDER, f"cricket_{today}.json")


def load_existing_data(output_file: str) -> Optional[Dict[str, Any]]:
    today = datetime.now().strftime("%Y-%m-%d")
    mgr = get_storage_manager()
    try:
        data = mgr.load_master(today)
        if data:
            return data
    except Exception:
        logging.debug("Mongo load failed; falling back to JSON")

    # Fallback to file
    if os.path.exists(output_file):
        try:
            import json
            with open(output_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    return None


def save_data(output_file: str, data: Dict[str, Any]) -> None:
    mgr = get_storage_manager()
    try:
        # StorageManager handles Mongo first then JSON fallback
        mgr.save_master(data)
        logging.info(f"Saved via StorageManager: {data.get('date')}")
    except Exception as e:
        logging.error(f"StorageManager save failed: {e}")
