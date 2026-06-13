from contextlib import asynccontextmanager
import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.matches import router as matches_router
from scraper.live_scraper import run_live_scraper


scraper_task = None


@asynccontextmanager
async def lifespan(app: FastAPI):

    global scraper_task

    print("Starting scraper...")

    scraper_task = asyncio.create_task(
        run_live_scraper()
    )

    yield

    if scraper_task:
        scraper_task.cancel()


app = FastAPI(
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    matches_router,
    prefix="/api"
)