import os
import json

from datetime import datetime

from config.settings import DATA_FOLDER

from db.mongodb import matches_collection


def get_output_path():

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    return os.path.join(
        DATA_FOLDER,
        f"cricket_{today}.json"
    )


def load_existing_data(output_file):

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    # MongoDB First

    mongo_data = matches_collection.find_one(
        {"date": today},
        {"_id": 0}
    )

    if mongo_data:
        return mongo_data

    # Fallback JSON

    if os.path.exists(output_file):

        try:

            with open(
                output_file,
                "r",
                encoding="utf-8"
            ) as f:

                return json.load(f)

        except Exception:
            pass

    return None


def save_data(output_file, data):

    # JSON SAVE

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )

    # MONGODB SAVE

    matches_collection.replace_one(
        {"date": data["date"]},
        data,
        upsert=True
    )

    print(
        f"Saved to JSON + MongoDB : {data['date']}"
    )