# ─── CONFIG ───────────────────────────────────────────────
from dotenv import load_dotenv
import os

load_dotenv()

TARGET_URL = "https://sportcenter.sir.sportradar.com/cricket-lmt"

LIVE_INTERVAL = 60       # seconds — live match update interval

DATA_FOLDER = "data"

LOG_FOLDER = "logs"

# ──────────────────────────────────────────────────────────
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME") or "cricket_db"
COLLECTION_NAME = os.getenv("COLLECTION_NAME") or "matches"
JSON_BACKUP_PATH = os.getenv("JSON_BACKUP_PATH") or DATA_FOLDER
SYNC_INTERVAL = int(os.getenv("SYNC_INTERVAL") or 30)
LOG_LEVEL = os.getenv("LOG_LEVEL") or "INFO"