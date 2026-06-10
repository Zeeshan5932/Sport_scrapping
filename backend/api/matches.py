from fastapi import APIRouter
from pathlib import Path
import json

router = APIRouter()

DATA_DIR = Path("../data/")


@router.get("/matches")
async def get_matches(date: str):

    """
    Frontend sends:
    2026-06-05

    File:
    05-06-2026.json
    """

    try:

        parts = date.split("-")

        formatted_date = (
            f"{parts[2]}-"
            f"{parts[1]}-"
            f"{parts[0]}"
        )

        file_path = (
            DATA_DIR /
            f"{formatted_date}.json"
        )

        print("READING:", file_path)

        if not file_path.exists():

            return {
                "error": "File not found"
            }

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        return data

    except Exception as e:

        return {
            "error": str(e)
        }