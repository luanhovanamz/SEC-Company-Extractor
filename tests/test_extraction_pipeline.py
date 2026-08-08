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
    print("SEC END-TO-END EXTRACTION PIPELINE TEST")
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

        extraction_service = ExtractionService()

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
        print()

        company = pipeline.extract_first(
            form="8-K",
            state="ME",
            start_date="2026-08-04",
            end_date="2026-08-04",
        )

        print()
        print("=" * 60)
        print("EXTRACTION RESULT")
        print("=" * 60)

        print()
        print("Company name:")
        print(company.company_name)

        print()
        print("CIK:")
        print(company.cik)

        print()
        print("Accession number:")
        print(company.accession_number)

        print()
        print("State of incorporation:")
        print(company.state_of_incorporation)

        print()
        print("Commission File Number:")
        print(company.commission_file_number)

        print()
        print(
            "IRS Employer Identification Number:"
        )
        print(
            company.employer_identification_number
        )

        print()
        print("Business address:")
        print(company.business_address)

        print()
        print("City:")
        print(company.city)

        print()
        print("State:")
        print(company.state)

        print()
        print("ZIP:")
        print(company.zip_code)

        print()
        print("Phone:")
        print(company.phone)

        print()
        print("President:")
        print(
            company.president
            or "(not found)"
        )

        print()
        print("CEO:")
        print(
            company.ceo
            or "(not found)"
        )

        print()
        print("Executives:")

        for executive in company.executives:
            print(
                f"- {executive.name} | "
                f"{executive.title}"
            )

        print()
        print("=" * 60)
        print("END-TO-END PIPELINE TEST: PASSED")
        print("=" * 60)

    finally:
        http.close()


if __name__ == "__main__":
    main()