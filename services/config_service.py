from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ConfigService:
    """Service for loading and saving application settings."""

    def __init__(self, settings_file: Path) -> None:
        self._settings_file = settings_file
        self._settings: dict[str, Any] = {}

    def load(self) -> None:
        """Load settings from JSON file."""
        if not self._settings_file.exists():
            raise FileNotFoundError(
                f"Settings file not found: {self._settings_file}"
            )

        with self._settings_file.open("r", encoding="utf-8-sig") as file:
            self._settings = json.load(file)

    def save(self) -> None:
        """Save settings to JSON file."""
        with self._settings_file.open("w", encoding="utf-8-sig") as file:
            json.dump(
                self._settings,
                file,
                indent=4,
                ensure_ascii=False,
            )

    def get(self, *keys: str, default: Any = None) -> Any:
        """Get a nested setting value."""
        value: Any = self._settings

        for key in keys:
            if not isinstance(value, dict):
                return default

            value = value.get(key)

            if value is None:
                return default

        return value

    def set(self, value: Any, *keys: str) -> None:
        """Set a nested setting value."""
        if not keys:
            raise ValueError("At least one key is required.")

        current = self._settings

        for key in keys[:-1]:
            current = current.setdefault(key, {})

        current[keys[-1]] = value
