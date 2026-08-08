from sec.http_client import HttpClient
from sec.search_client import SearchClient


def main() -> None:
    http = HttpClient(
        user_agent="SEC Company Extractor (luanhovanamz@gmail.com)"
    )

    try:
        client = SearchClient(http)

        print("=" * 70)
        print("SEC Pagination Investigation")
        print("=" * 70)

        print("\nRequest 1: default")
        
        filings_1 = client.search(
            form="8-K",
            state="ME",
            start_date="2021-08-07",
            end_date="2026-08-07",
        )

        print("Returned:", len(filings_1))

        if filings_1:
            print(
                "First:",
                filings_1[0].accession_number,
            )
            print(
                "Last:",
                filings_1[-1].accession_number,
            )

        print("\nRequest 2: from_index=100")

        filings_2 = client.search(
            form="8-K",
            state="ME",
            start_date="2021-08-07",
            end_date="2026-08-07",
            from_index=100,
        )

        print("Returned:", len(filings_2))

        if filings_2:
            print(
                "First:",
                filings_2[0].accession_number,
            )
            print(
                "Last:",
                filings_2[-1].accession_number,
            )

        print("\nComparison")
        print("-" * 70)

        if filings_1 and filings_2:
            same_first = (
                filings_1[0].accession_number
                == filings_2[0].accession_number
            )

            print("Same first filing:", same_first)

            if same_first:
                print(
                    "\nWARNING:"
                    "\nSEC returned the same first page."
                    "\nThe from_index parameter is currently"
                    "\nnot being sent to the SEC endpoint."
                )
            else:
                print(
                    "\nPagination parameter appears to work."
                )

        print("=" * 70)

    finally:
        http.close()


if __name__ == "__main__":
    main()