from sec.http_client import HttpClient
from sec.search_client import SearchClient
from sec.filing_downloader import FilingDownloader

from services.extraction_service import ExtractionService
from services.extraction_pipeline import ExtractionPipeline


USER_AGENT = (
    "SEC Company Extractor "
    "(luanhovanamz@gmail.com)"
)


def main() -> None:
    print("=" * 60)
    print("SEC BATCH EXTRACTION TEST")
    print("=" * 60)

    http = HttpClient(
        user_agent=USER_AGENT
    )

    try:
        search_client = SearchClient(
            http
        )

        filing_downloader = FilingDownloader(
            http,
            download_folder="cache",
        )

        extraction_service = (
            ExtractionService()
        )

        pipeline = ExtractionPipeline(
            search_client=search_client,
            filing_downloader=filing_downloader,
            extraction_service=extraction_service,
        )

        print()
        print("Searching SEC filings...")
        print("Form: 8-K")
        print("State: ME")
        print("Date: 2026-08-04")
        print("Maximum filings: 3")
        print()

        companies = pipeline.extract_many(
            form="8-K",
            state="ME",
            start_date="2026-08-04",
            end_date="2026-08-04",
            size=3,
        )

        print()
        print("=" * 60)
        print("BATCH EXTRACTION RESULT")
        print("=" * 60)

        print()
        print("Companies extracted:")
        print(len(companies))

        for index, company in enumerate(
            companies,
            start=1,
        ):
            print()
            print(f"--- Company {index} ---")

            print(
                "Company:",
                company.company_name,
            )

            print(
                "CIK:",
                company.cik,
            )

            print(
                "Accession:",
                company.accession_number,
            )

            print(
                "State:",
                company.state,
            )

            print(
                "Phone:",
                company.phone,
            )

        print()
        print("=" * 60)
        print("BATCH EXTRACTION TEST: PASSED")
        print("=" * 60)

    finally:
        http.close()


if __name__ == "__main__":
    main()