import os
from datetime import datetime
from time import time


def set_environment() -> None:
    if "HEGELAI_URL" not in os.environ:
        os.environ["HEGELAI_URL"] = "https://hegel-ai.com/api/log/add"
    if "HEGELAI_FEEDBACK_URL" not in os.environ:
        os.environ["HEGELAI_FEEDBACK_URL"] = "https://hegel-ai.com/api/log/update"
    if os.environ.get("DEBUG", default=False):
        os.environ["HEGELAI_URL"] = "http://localhost:3001/api/log/add"
        os.environ["HEGELAI_FEEDBACK_URL"] = "http://localhost:3001/api/log/update"
    if "HEGELAI_API_KEY" not in os.environ:
        raise ValueError("Please set your HEGELAI_API_KEY.")


def get_current_time_millis() -> int:
    return int(time() * 1000)


def get_present_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")
