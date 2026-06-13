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