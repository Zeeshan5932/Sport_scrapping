import asyncio
import logging

from .storage_manager import get_storage_manager


async def start_sync_loop():
    mgr = get_storage_manager()
    logging.info("Starting storage sync loop")
    await mgr.sync_loop()
