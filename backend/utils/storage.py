import os
import json
from datetime import datetime

from config.settings import DATA_FOLDER


def get_output_path():
    today = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(DATA_FOLDER, f"cricket_{today}.json")


def load_existing_data(output_file):
    """Existing JSON load karo — taake ended matches dobara scrape na hon."""
    if os.path.exists(output_file):
        try:
            with open(output_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    return None


def save_data(output_file, data):
    """Turant save karo."""
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)