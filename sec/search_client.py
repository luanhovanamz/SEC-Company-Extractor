from __future__ import annotations

from typing import Any

from models.filing import Filing
from sec.http_client import HttpClient


class SearchClient:
    """Client for the SEC EDGAR Search API."""

    SEARCH_API = "https://efts.sec.gov/LATEST/search-index"

    def __init__(self, http_client: HttpClient) -> None:
        self._http = http_client

    @staticmethod
    def _extract_primary_document(
        record: dict[str, Any],
    ) -> str:
        """
        Extract the primary document from the SEC search record ID.

        Example:

        0001104659-26-090033:tm2622041d1_8k.htm

        becomes:

        tm2622041d1_8k.htm
        """

        record_id = str(record.get("_id", ""))

        if ":" in record_id:
            return record_id.split(":", 1)[1]

        return ""

    @staticmethod
    def _extract_company_name(
        source: dict[str, Any],
    ) -> str:
        """Extract a clean company name from display_names."""

        display_names = source.get("display_names", [])

        if not display_names:
            return ""

        name = str(display_names[0]).strip()

        marker = "  (CIK "

        if marker in name:
            name = name.split(marker, 1)[0].strip()

        return name

    @staticmethod
    def _first_value(
        values: Any,
        default: str = "",
    ) -> str:
        """Return the first value from a SEC list field."""

        if isinstance(values, list) and values:
            return str(values[0])

        if values is None:
            return default

        return str(values)

    def search(
        self,
        form: str,
        state: str,
        start_date: str,
        end_date: str,
        from_index: int = 0,
        size: int = 100,
    ) -> list[Filing]:
        """
        Search SEC filings and convert results into Filing objects.

        Parameters
        ----------
        form:
            SEC filing form, for example 8-K.

        state:
            State code, for example ME.

        start_date:
            Search start date in YYYY-MM-DD format.

        end_date:
            Search end date in YYYY-MM-DD format.

        from_index:
            Pagination offset.

        size:
            Number of records requested per page.
        """

        params = {
            "locationCode": state,
            "locationCodes": state,
            "filter_forms": form,
            "startdt": start_date,
            "enddt": end_date,
            "from": from_index,
            "size": size,
        }

        response = self._http.get(
            self.SEARCH_API,
            params=params,
        )

        result = response.json()

        if not isinstance(result, dict):
            raise ValueError(
                "SEC Search API returned invalid JSON."
            )

        hits = result.get("hits", {})

        if not isinstance(hits, dict):
            return []

        records = hits.get("hits", [])

        if not isinstance(records, list):
            return []

        filings: list[Filing] = []

        for record in records:
            if not isinstance(record, dict):
                continue

            source = record.get("_source", {})

            if not isinstance(source, dict):
                continue

            cik = self._first_value(
                source.get("ciks")
            )

            filing = Filing(
                accession_number=str(
                    source.get("adsh", "")
                ),
                cik=cik,
                company_name=self._extract_company_name(
                    source
                ),
                form=str(
                    source.get("form", "")
                ),
                filing_date=str(
                    source.get("file_date", "")
                ),
                business_state=self._first_value(
                    source.get("biz_states")
                ),
                business_location=self._first_value(
                    source.get("biz_locations")
                ),
                primary_document=self._extract_primary_document(
                    record
                ),
            )

            filings.append(filing)

        return filings


if __name__ == "__main__":
    print("SearchClient module loaded successfully.")