from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import logging

from api.matches import router as matches_router
from storage.storage_manager import StorageManager, set_storage_manager
from scraper.live_scraper import run_live_scraper
from config import settings
import subprocess

subprocess.run(
    ["python", "-m", "playwright", "install", "chromium"],
    check=True
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup logging
    logging.basicConfig(level=getattr(logging, getattr(settings, "LOG_LEVEL", "INFO")))

    # Initialize storage manager and set as global
    mgr = StorageManager()
    set_storage_manager(mgr)

    # Start background tasks
    loop = asyncio.get_event_loop()

    sync_task = loop.create_task(mgr.sync_loop())

    async def scraper_supervisor():
        while True:
            try:
                await run_live_scraper()
            except asyncio.CancelledError:
                break
            except Exception:
                logging.exception("Scraper crashed; restarting after delay")
                await asyncio.sleep(5)

    scraper_task = loop.create_task(scraper_supervisor())

    try:
        yield
    finally:
        sync_task.cancel()
        scraper_task.cancel()
        await asyncio.gather(sync_task, scraper_task, return_exceptions=True)


app = FastAPI(title="Cricket API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(matches_router, prefix="/api")
from api.health import router as health_router
app.include_router(health_router, prefix="/api")


@app.get("/")
def root():
    return {"status": "running"}


if __name__ == "__main__":
    import uvicorn
    import sys

    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        logging.info("Shutdown requested (KeyboardInterrupt)")
        sys.exit(0)