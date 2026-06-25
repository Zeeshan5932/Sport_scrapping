"""
Virtual display manager for headless Linux servers (Render, Railway, etc.)
Starts Xvfb so Playwright can run with headless=False on servers with no display.
"""

import os
import logging
import subprocess
import time


_xvfb_process = None


def start_virtual_display(display: str = ":99", screen: str = "0", resolution: str = "1400x900x24"):
    """
    Start Xvfb virtual display.
    Call this ONCE before launching Playwright browser.
    Safe to call on local machines too — detects if display already exists.
    """
    global _xvfb_process

    # Local machine with real display — skip
    if os.environ.get("DISPLAY") and not _is_server_environment():
        logging.info(f"Real display detected ({os.environ.get('DISPLAY')}) — skipping Xvfb")
        return

    if _xvfb_process and _xvfb_process.poll() is None:
        logging.info("Xvfb already running")
        return

    try:
        cmd = ["Xvfb", display, "-screen", screen, resolution, "-ac", "+extension", "GLX"]
        _xvfb_process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # Wait for display to be ready
        time.sleep(2)

        # Set DISPLAY env var so Playwright finds it
        os.environ["DISPLAY"] = display

        if _xvfb_process.poll() is None:
            logging.info(f"Xvfb started on display {display}")
        else:
            logging.error("Xvfb failed to start")

    except FileNotFoundError:
        logging.warning("Xvfb not found — install it with: apt-get install xvfb")
    except Exception as e:
        logging.error(f"Xvfb start error: {e}")


def stop_virtual_display():
    """Stop Xvfb — call on shutdown."""
    global _xvfb_process
    if _xvfb_process and _xvfb_process.poll() is None:
        _xvfb_process.terminate()
        _xvfb_process.wait()
        logging.info("Xvfb stopped")


def _is_server_environment() -> bool:
    """Detect if running on a server (no real display available)."""
    # Render, Railway, Heroku etc. set these
    return any([
        os.environ.get("RENDER"),
        os.environ.get("RAILWAY_ENVIRONMENT"),
        os.environ.get("HEROKU_APP_NAME"),
        os.environ.get("CI"),
        not os.environ.get("DISPLAY"),
    ])