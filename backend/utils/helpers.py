"""
MINDFORGE — Shared Helpers
"""
import re
from typing import Optional


def truncate(text: str, max_len: int = 200) -> str:
    """Truncate text to max_len characters with ellipsis."""
    return text if len(text) <= max_len else text[:max_len] + "..."


def clean_html(html: str) -> str:
    """Strip HTML tags from a string."""
    return re.sub(r"<[^>]+>", "", html).strip()


def is_valid_url(url: str) -> bool:
    """Basic URL validation."""
    pattern = re.compile(
        r"^https?://"
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"
        r"localhost|"
        r"\d{1,3}(?:\.\d{1,3}){3})"
        r"(?::\d+)?"
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )
    return bool(pattern.match(url))


def sanitize_filename(name: str) -> str:
    """Make a string safe for use as a filename."""
    return re.sub(r"[^a-zA-Z0-9_\-.]", "_", name)
