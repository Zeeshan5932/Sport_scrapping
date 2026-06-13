# Sport Scrapping Backend

## Overview

This project is a cricket live match scraping backend built using:

* Python
* Playwright
* FastAPI
* JSON Storage

The scraper continuously scrapes cricket match data from SportRadar and stores the results in JSON files.

The FastAPI server reads these JSON files and provides APIs for frontend applications.

---

# Project Structure

backend/

├── api/

│   └── matches.py

│

├── scraper/

│   ├── live_scraper.py

│   └── extractors.py

│

├── utils/

│   ├── storage.py

│   ├── match_utils.py

│   └── logger.py

│

├── config/

│   └── settings.py

│

├── data/

│   └── cricket_YYYY-MM-DD.json

│

├── main.py

├── requirements.txt

└── README.md

---

# Data Flow

Scraper

↓

SportRadar Website

↓

Playwright Scraping

↓

JSON File

↓

FastAPI

↓

Frontend

---

# JSON Output

The scraper saves files in:

data/

Example:

cricket_2026-06-13.json

Structure:

{
"date": "2026-06-13",
"tournaments": [
{
"tournament_name": "Tournament",
"matches": []
}
]
}

---

# Installation

## Create Virtual Environment

Windows

python -m venv venv

Activate

venv\Scripts\activate

---

# Install Requirements

pip install -r requirements.txt

---

# Install Playwright

playwright install

---

# Run Scraper

The scraper continuously updates live scores and stores data inside the data folder.

Command:

python main.py

The scraper:

* Opens Playwright browser
* Scrapes matches
* Updates scores every 60 seconds
* Saves data automatically

Generated files:

data/cricket_YYYY-MM-DD.json

Example:

data/cricket_2026-06-13.json

---

# Run FastAPI Server

Open a new terminal.

Activate venv:

venv\Scripts\activate

Start API:

uvicorn main:app --reload

or

uvicorn main:app

Recommended:

uvicorn main:app

---

# API Endpoints

Base URL

http://localhost:8000

---

## Get Matches By Date

GET

/api/matches?date=2026-06-13

Response:

{
"date": "2026-06-13",
"tournaments": [...]
}

---

## Get Single Match

GET

/api/match/{match_id}?date=2026-06-13

Example:

/api/match/71742764?date=2026-06-13

Response:

{
"match_id": "71742764",
"home_team": "...",
"away_team": "...",
"innings": [...]
}

---

# Frontend Integration

Frontend should call:

GET /api/matches?date=YYYY-MM-DD

to load all matches.

Frontend should call:

GET /api/match/{match_id}?date=YYYY-MM-DD

to load a single match.

Important fields:

match.match_id

match.home_team

match.away_team

match.home_score

match.away_score

match.status

match.result

---

# Running Both Together

Terminal 1

python main.py

This runs the scraper.

Terminal 2

uvicorn main:app

This runs the API server.

---

# Development Workflow

1. Start scraper

python main.py

2. Verify JSON file created

data/cricket_YYYY-MM-DD.json

3. Start FastAPI

uvicorn main:app

4. Test APIs

/api/matches?date=YYYY-MM-DD

/api/match/{match_id}?date=YYYY-MM-DD

5. Connect frontend

---

# Deployment Notes

Recommended:

* Railway
* VPS
* DigitalOcean
* AWS EC2

Do not use static hosting because Playwright requires a running server.

Production Flow:

Server Start

↓

Scraper Start

↓

JSON Update

↓

FastAPI Reads JSON

↓

Frontend Calls API

---

# Important Notes

The scraper and API are separate processes.

Scraper Responsibility:

* Collect data
* Update JSON files

API Responsibility:

* Read JSON files
* Return data to frontend

This architecture is stable and easier to maintain.

---

# Current Date File Format

cricket_YYYY-MM-DD.json

Example:

cricket_2026-06-13.json

The API expects the same date format when requesting data.

Example:

/api/matches?date=2026-06-13
