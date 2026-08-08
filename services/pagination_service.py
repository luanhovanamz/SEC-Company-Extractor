from __future__ import annotations

from models.filing import Filing
from sec.search_client import SearchClient


class PaginationService:
    """
    Retrieve all SEC filings by requesting multiple pages.

    Filings are deduplicated using accession_number.
    """

    def __init__(
        self,
        search_client: SearchClient,
        page_size: int = 100,
    ) -> None:
        if page_size <= 0:
            raise ValueError("page_size must be greater than zero.")

        self._search_client = search_client
        self._page_size = page_size

    def search_all(
        self,
        form: str,
        state: str,
        start_date: str,
        end_date: str,
        max_records: int | None = None,
    ) -> list[Filing]:
        """
        Retrieve all available filings.

        Parameters
        ----------
        form:
            SEC form, for example 8-K.

        state:
            State code, for example ME.

        start_date:
            Start date in YYYY-MM-DD.

        end_date:
            End date in YYYY-MM-DD.

        max_records:
            Optional safety limit.
            None means no artificial limit.
        """

        unique_filings: dict[str, Filing] = {}

        offset = 0

        while True:
            print(
                f"Requesting SEC records "
                f"from={offset}, size={self._page_size}"
            )

            filings = self._search_client.search(
                form=form,
                state=state,
                start_date=start_date,
                end_date=end_date,
                from_index=offset,
                size=self._page_size,
            )

            if not filings:
                print("No more records returned.")
                break

            before_count = len(unique_filings)

            for filing in filings:
                accession = filing.accession_number.strip()

                if not accession:
                    continue

                unique_filings[accession] = filing

                if (
                    max_records is not None
                    and len(unique_filings) >= max_records
                ):
                    break

            added = len(unique_filings) - before_count

            print(
                f"Received: {len(filings)} | "
                f"New unique: {added} | "
                f"Total unique: {len(unique_filings)}"
            )

            if (
                max_records is not None
                and len(unique_filings) >= max_records
            ):
                print("Maximum record limit reached.")
                break

            # If SEC returns fewer records than the requested
            # page size, this is normally the final page.
            if len(filings) < self._page_size:
                print("Final page reached.")
                break

            offset += self._page_size

        return list(unique_filings.values())