from sec.http_client import HttpClient
from sec.search_client import SearchClient
from services.pagination_service import PaginationService


def main() -> None:
    http = HttpClient(
        user_agent="SEC Company Extractor (luanhovanamz@gmail.com)"
    )

    try:
        search_client = SearchClient(http)

        pagination = PaginationService(
            search_client=search_client,
            page_size=100,
        )

        filings = pagination.search_all(
            form="8-K",
            state="ME",
            start_date="2021-08-07",
            end_date="2026-08-07",
        )

        print("=" * 70)
        print("SEC Pagination Service Test")
        print("=" * 70)

        print("Total unique filings:", len(filings))

        if filings:
            print("\nFirst filing:")
            print(filings[0])

            print("\nLast filing:")
            print(filings[-1])

        accession_numbers = [
            filing.accession_number
            for filing in filings
        ]

        print(
            "\nUnique accession numbers:",
            len(set(accession_numbers)),
        )

        print("=" * 70)

    finally:
        http.close()


if __name__ == "__main__":
    main()