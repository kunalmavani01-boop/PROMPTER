from __future__ import annotations

import threading
import time
import webbrowser

import uvicorn

from main import DEFAULT_HOST, DEFAULT_PORT, app


def open_browser() -> None:
    time.sleep(1.2)
    webbrowser.open(f"http://{DEFAULT_HOST}:{DEFAULT_PORT}")


if __name__ == "__main__":
    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run(app, host=DEFAULT_HOST, port=DEFAULT_PORT)
