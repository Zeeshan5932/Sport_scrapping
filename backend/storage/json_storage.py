from typing import Optional, Any, Dict
import json
import os
import logging
from datetime import datetime

from config import settings


class JSONStorage:
    def __init__(self, data_folder: Optional[str] = None, pending_file: Optional[str] = None) -> None:
        self.data_folder = data_folder or settings.DATA_FOLDER or "data"
        os.makedirs(self.data_folder, exist_ok=True)
        # No pending.json usage; daily files only

    def _daily_path(self, date: str) -> str:
        return os.path.join(self.data_folder, f"cricket_{date}.json")

    def load_master(self, date: str) -> Optional[Dict[str, Any]]:
        p = self._daily_path(date)
        if not os.path.exists(p):
            return None
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logging.warning(f"Failed to load JSON {p}: {e}")
            return None

    def save_master(self, data: Dict[str, Any]) -> None:
        p = self._daily_path(data.get("date", datetime.now().strftime("%Y-%m-%d")))
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def append_pending(self, data: Dict[str, Any]) -> None:
        # Deprecated: pending queue not used. Use save_master() to write daily file only.
        self.save_master(data)

    def load_pending(self) -> list:
        # No pending file; return empty list
        return []

    def clear_pending(self, keep_dates: Optional[set] = None) -> None:
        # No pending file to clear
        return

    def list_daily_files(self) -> list:
        """Return list of dates for which daily backup files exist."""
        files = []
        try:
            for name in os.listdir(self.data_folder):
                if name.startswith("cricket_") and name.endswith(".json"):
                    # cricket_YYYY-MM-DD.json
                    parts = name[len("cricket_"):-5]
                    files.append(parts)
        except Exception:
            pass
        return files
