import os
import logging

from config.settings import DATA_FOLDER, LOG_FOLDER


def setup_logging():
    os.makedirs(LOG_FOLDER, exist_ok=True)
    os.makedirs(DATA_FOLDER, exist_ok=True)

    log_file = os.path.join(LOG_FOLDER, "scraper.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )