from pathlib import Path
import json

from fastapi import APIRouter

router = APIRouter()

DATA_DIR = Path("data")


@router.get("/matches")
async def get_matches(date: str):

    file_path = (
        DATA_DIR /
        f"cricket_{date}.json"
    )

    if not file_path.exists():

        return {
            "date": date,
            "tournaments": []
        }

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


@router.get("/match/{match_id}")
async def get_match(
    match_id: str,
    date: str
):

    file_path = (
        DATA_DIR /
        f"cricket_{date}.json"
    )

    if not file_path.exists():
        return {}

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    for tournament in data.get(
        "tournaments",
        []
    ):

        for match in tournament.get(
            "matches",
            []
        ):

            if str(
                match.get("match_id")
            ) == str(match_id):

                return match

    return {}