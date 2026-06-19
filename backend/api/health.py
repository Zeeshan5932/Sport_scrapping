from fastapi import APIRouter
import logging
from storage.storage_manager import get_storage_manager

router = APIRouter()


@router.get("/health")
async def health():
    mgr = get_storage_manager()
    try:
        mongo_ok = mgr.mongo.is_available()
    except Exception:
        mongo_ok = False

    # Count local daily backups that are not yet present in Mongo
    pending_count = 0
    try:
        files = mgr.json.list_daily_files()
        for d in files:
            try:
                if not mgr.mongo.is_available():
                    pending_count += 1
                else:
                    if not mgr.mongo.load_master(d):
                        pending_count += 1
            except Exception:
                pending_count += 1
    except Exception:
        pending_count = 0

    return {"status": "ok", "mongo": mongo_ok, "pending_count": pending_count}
