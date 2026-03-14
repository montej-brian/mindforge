"""
MINDFORGE — Structured Logger
"""
import logging
import logging.handlers
import sys
from pathlib import Path

from config import settings


def setup_logger():
    """Configure the root logger with console + rotating file handlers."""
    level = getattr(logging, settings.log_level.upper(), logging.INFO)

    # Ensure log directory exists
    log_path = Path(settings.log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(fmt)
    console.setLevel(level)

    # Rotating file handler (10 MB × 5 backups)
    file_handler = logging.handlers.RotatingFileHandler(
        settings.log_file, maxBytes=10 * 1024 * 1024, backupCount=5
    )
    file_handler.setFormatter(fmt)
    file_handler.setLevel(level)

    root = logging.getLogger()
    root.setLevel(level)
    root.addHandler(console)
    root.addHandler(file_handler)

    # Suppress noisy third-party loggers
    for name in ("urllib3", "selenium", "httpx", "httpcore"):
        logging.getLogger(name).setLevel(logging.WARNING)
