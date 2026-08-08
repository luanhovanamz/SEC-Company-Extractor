from __future__ import annotations

import re
from pathlib import Path

from bs4 import BeautifulSoup


class FilingParser:
    """Parse SEC filing HTML documents."""

    def __init__(self, file_path: str | Path) -> None:
        self._file_path = Path(file_path)

        if not self._file_path.exists():
            raise FileNotFoundError(
                f"Filing not found: {self._file_path}"
            )

    def read_html(self) -> str:
        """Read the raw HTML filing."""

        return self._file_path.read_text(
            encoding="utf-8",
            errors="replace",
        )

    def parse(self) -> BeautifulSoup:
        """Create a BeautifulSoup document."""

        html = self.read_html()

        return BeautifulSoup(
            html,
            "html.parser",
        )

    def get_text(self) -> str:
        """
        Extract visible text from the filing.

        Scripts, styles and other non-content elements
        are removed.
        """

        soup = self.parse()

        for element in soup(
            ["script", "style", "noscript"]
        ):
            element.decompose()

        text = soup.get_text(
            separator="\n"
        )

        lines = []

        for line in text.splitlines():
            line = re.sub(
                r"\s+",
                " ",
                line,
            ).strip()

            if line:
                lines.append(line)

        return "\n".join(lines)

    def save_text(
        self,
        output_path: str | Path,
    ) -> Path:
        """Save cleaned filing text for analysis."""

        output = Path(output_path)

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output.write_text(
            self.get_text(),
            encoding="utf-8",
        )

        return output