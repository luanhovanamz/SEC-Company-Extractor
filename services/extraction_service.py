from __future__ import annotations

from pathlib import Path

from models.company import Company
from services.company_extractor import CompanyExtractor
from services.filing_parser import FilingParser


class ExtractionService:
    """
    Orchestrate SEC filing parsing and company extraction.
    """

    def __init__(
        self,
        output_directory: str | Path = "temp/filing",
    ) -> None:
        self._output_directory = Path(
            output_directory
        )

    def extract_from_file(
        self,
        filing_path: str | Path,
        *,
        accession_number: str = "",
        cik: str = "",
    ) -> Company:
        """
        Parse an SEC HTML filing from disk and
        extract structured company information.
        """

        filing_path = Path(filing_path)

        if not filing_path.exists():
            raise FileNotFoundError(
                f"Filing not found: {filing_path}"
            )

        parser = FilingParser(
            filing_path
        )

        text = parser.get_text()

        return self.extract_from_text(
            text,
            source_filing=str(filing_path),
            accession_number=accession_number,
            cik=cik,
        )

    def extract_from_text(
        self,
        text: str,
        *,
        source_filing: str = "",
        accession_number: str = "",
        cik: str = "",
    ) -> Company:
        """
        Extract structured company information
        from already-cleaned SEC filing text.
        """

        if not text or not text.strip():
            raise ValueError(
                "Filing text cannot be empty."
            )

        extractor = CompanyExtractor(
            text=text,
            source_filing=source_filing,
        )

        company = extractor.extract()

        company.accession_number = (
            accession_number
        )

        company.cik = cik

        return company

    def extract_from_text_file(
        self,
        text_file: str | Path,
        *,
        accession_number: str = "",
        cik: str = "",
    ) -> Company:
        """
        Read an already-cleaned SEC text file
        and extract structured company information.
        """

        text_file = Path(text_file)

        if not text_file.exists():
            raise FileNotFoundError(
                f"Text file not found: {text_file}"
            )

        text = text_file.read_text(
            encoding="utf-8",
            errors="replace",
        )

        return self.extract_from_text(
            text,
            source_filing=str(text_file),
            accession_number=accession_number,
            cik=cik,
        )