from __future__ import annotations

from pathlib import Path

from sec.http_client import HttpClient


class FilingDownloader:
    """Download SEC filing documents from EDGAR Archives."""

    BASE_ARCHIVES = "https://www.sec.gov/Archives/edgar/data"

    def __init__(
        self,
        http: HttpClient,
        download_folder: str = "cache",
    ) -> None:
        self._http = http
        self._folder = Path(download_folder)
        self._folder.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def normalize_cik(cik: str) -> str:
        """Convert SEC CIK to the numeric archive path."""

        return str(cik).strip().lstrip("0") or "0"

    @staticmethod
    def normalize_accession(accession_number: str) -> str:
        """Remove dashes from an SEC accession number."""

        return accession_number.replace("-", "").strip()

    def build_url(
        self,
        cik: str,
        accession_number: str,
        primary_document: str,
    ) -> str:
        """
        Build the official SEC EDGAR archive URL.

        Example:

        CIK:
            0000874716

        Accession:
            0001104659-26-090033

        Document:
            tm2622041d1_8k.htm

        Result:

        https://www.sec.gov/Archives/edgar/data/874716/
        000110465926090033/tm2622041d1_8k.htm
        """

        cik_normalized = self.normalize_cik(cik)

        accession_normalized = self.normalize_accession(
            accession_number
        )

        document = primary_document.strip().lstrip("/")

        return (
            f"{self.BASE_ARCHIVES}/"
            f"{cik_normalized}/"
            f"{accession_normalized}/"
            f"{document}"
        )

    def download(
        self,
        cik: str,
        accession_number: str,
        primary_document: str,
    ) -> Path:
        """Download a filing document and save it locally."""

        url = self.build_url(
            cik=cik,
            accession_number=accession_number,
            primary_document=primary_document,
        )

        response = self._http.get(url)

        output_file = self._folder / primary_document

        output_file.write_bytes(response.content)

        return output_file