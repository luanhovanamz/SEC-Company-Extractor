from __future__ import annotations

from pathlib import Path

from models.company import Company
from models.filing import Filing

from sec.filing_downloader import FilingDownloader
from sec.search_client import SearchClient

from services.extraction_service import ExtractionService


class ExtractionPipeline:
    """
    End-to-end SEC company extraction pipeline.

    Flow:

        SearchClient
            ↓
        Filing
            ↓
        FilingDownloader
            ↓
        HTML filing
            ↓
        ExtractionService
            ↓
        Company
    """

    def __init__(
        self,
        search_client: SearchClient,
        filing_downloader: FilingDownloader,
        extraction_service: ExtractionService,
    ) -> None:
        self._search_client = search_client
        self._filing_downloader = filing_downloader
        self._extraction_service = extraction_service

    def extract_first(
        self,
        *,
        form: str,
        state: str,
        start_date: str,
        end_date: str,
    ) -> Company:
        """
        Search SEC filings, download the first filing,
        and extract company information.
        """

        filings = self._search_client.search(
            form=form,
            state=state,
            start_date=start_date,
            end_date=end_date,
            size=1,
        )

        if not filings:
            raise ValueError(
                "No SEC filings found."
            )

        filing = filings[0]

        if not isinstance(filing, Filing):
            raise TypeError(
                "SearchClient.search() must return "
                "Filing objects."
            )

        return self._extract_filing(filing)

    def extract_many(
        self,
        *,
        form: str,
        state: str,
        start_date: str,
        end_date: str,
        size: int = 10,
    ) -> list[Company]:
        """
        Search SEC filings and extract multiple companies.

        Parameters
        ----------
        form:
            SEC filing form, for example 8-K.

        state:
            Two-letter state code, for example ME.

        start_date:
            Search start date in YYYY-MM-DD format.

        end_date:
            Search end date in YYYY-MM-DD format.

        size:
            Maximum number of filings to process.
        """

        if size <= 0:
            raise ValueError(
                "size must be greater than zero."
            )

        filings = self._search_client.search(
            form=form,
            state=state,
            start_date=start_date,
            end_date=end_date,
            size=size,
        )

        if not filings:
            return []

        companies: list[Company] = []

        for filing in filings:
            if not isinstance(filing, Filing):
                continue

            try:
                company = self._extract_filing(
                    filing
                )

                companies.append(company)

            except Exception as exc:
                print(
                    "Failed to extract filing "
                    f"{filing.accession_number}: "
                    f"{exc}"
                )

        return companies

    def _extract_filing(
        self,
        filing: Filing,
    ) -> Company:
        """
        Download and extract one SEC filing.
        """

        accession_number = (
            filing.accession_number
        )

        cik = filing.cik

        primary_document = (
            filing.primary_document
        )

        if not accession_number:
            raise ValueError(
                "SEC filing does not contain "
                "an accession number."
            )

        if not cik:
            raise ValueError(
                "SEC filing does not contain CIK."
            )

        if not primary_document:
            raise ValueError(
                "SEC filing does not contain "
                "primary document."
            )

        filing_path = (
            self._filing_downloader.download(
                cik=cik,
                accession_number=accession_number,
                primary_document=primary_document,
            )
        )

        if not isinstance(
            filing_path,
            Path,
        ):
            filing_path = Path(
                filing_path
            )

        company = (
            self._extraction_service.extract_from_file(
                filing_path,
                accession_number=accession_number,
                cik=cik,
            )
        )

        return company