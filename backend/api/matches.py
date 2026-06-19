from fastapi import APIRouter, HTTPException
import logging
from storage.storage_manager import get_storage_manager
import asyncio
import os
import json
from config import settings

router = APIRouter()


@router.get("/matches")
async def get_matches(date: str):
    try:
        mgr = get_storage_manager()
        # normalize date formats
        try:
            date_norm = mgr.normalize_date(date)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid date format")

        data = mgr.load_master(date_norm)
        if not data:
            # Try to load local JSON backup directly as a last resort
            try:
                backup_path = os.path.join(settings.DATA_FOLDER, f"cricket_{date_norm}.json")
                if os.path.exists(backup_path):
                    with open(backup_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        logging.info(f"Loaded matches from local backup {backup_path}")
                        return data
            except Exception:
                logging.exception("Failed to load local JSON backup")

            # start background scrape for requested date (non-blocking)
            try:
                from scraper.live_scraper import scrape_date_once
                asyncio.create_task(scrape_date_once(date_norm))
            except Exception:
                logging.exception("Failed to start background scrape")

            return {"date": date_norm, "tournaments": []}

        return data
    except Exception as e:
        logging.exception(f"Error in get_matches: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/match/{match_id}")
async def get_match(match_id: str, date: str):
    try:
        mgr = get_storage_manager()
        try:
            date_norm = mgr.normalize_date(date)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid date format")

        data = mgr.load_master(date_norm)
        if not data:
            return {}

        for tournament in data.get("tournaments", []):
            for match in tournament.get("matches", []):
                if str(match.get("match_id")) == str(match_id):
                    return match

        return {}
    except Exception as e:
        logging.exception(f"Error in get_match: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")