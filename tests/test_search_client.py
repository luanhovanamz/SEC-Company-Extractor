from sec.http_client import HttpClient
from sec.search_client import SearchClient


def main() -> None:
    http = HttpClient(
        user_agent="SEC Company Extractor (luanhovanamz@gmail.com)"
    )

    try:
        client = SearchClient(http)

        filings = client.search(
            form="8-K",
            state="ME",
            start_date="2021-08-07",
            end_date="2026-08-07",
        )

        print("=" * 70)
        print("SEC Search Client Test")
        print("=" * 70)

        print("Returned filings:", len(filings))

        if filings:
            filing = filings[0]

            print("\nFirst Filing")
            print("-" * 70)
            print("Company          :", filing.company_name)
            print("CIK              :", filing.cik)
            print("Form             :", filing.form)
            print("Filing Date      :", filing.filing_date)
            print("Accession Number :", filing.accession_number)
            print("Business State   :", filing.business_state)
            print("Business Location:", filing.business_location)
            print("Primary Document :", filing.primary_document)

        print("=" * 70)

    finally:
        http.close()


if __name__ == "__main__":
    main()