from fastapi import APIRouter

from db.mongodb import matches_collection

router = APIRouter()


@router.get("/matches")
async def get_matches(date: str):

    data = matches_collection.find_one(
        {"date": date},
        {"_id": 0}
    )

    if not data:

        return {
            "date": date,
            "tournaments": []
        }

    return data


@router.get("/match/{match_id}")
async def get_match(
    match_id: str,
    date: str
):

    data = matches_collection.find_one(
        {"date": date},
        {"_id": 0}
    )

    if not data:
        return {}

    for tournament in data.get(
        "tournaments",
        []
    ):

        for match in tournament.get(
            "matches",
            []
        ):

            if (
                str(match.get("match_id"))
                == str(match_id)
            ):
                return match

    return {}