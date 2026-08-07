from __future__ import annotations

import logging
from pathlib import Path


class LoggerService:
    """Application logger."""

    def __init__(self, log_folder: Path) -> None:
        self._log_folder = log_folder
        self._log_folder.mkdir(parents=True, exist_ok=True)

        log_file = self._log_folder / "application.log"

        self._logger = logging.getLogger("SECExtractor")

        if self._logger.handlers:
            return

        self._logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        file_handler = logging.FileHandler(
            log_file,
            encoding="utf-8",
        )

        console_handler = logging.StreamHandler()

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self._logger.addHandler(file_handler)
        self._logger.addHandler(console_handler)

    @property
    def logger(self) -> logging.Logger:
        return self._logger