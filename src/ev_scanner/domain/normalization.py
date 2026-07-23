from __future__ import annotations

import unicodedata


def normalize_racing_name(value: str) -> str:
    """Return a deterministic matching key while preserving Unicode letters and digits."""
    normalized = unicodedata.normalize("NFKC", value).casefold().strip()
    tokenized = "".join(character if character.isalnum() else " " for character in normalized)
    return " ".join(tokenized.split())
