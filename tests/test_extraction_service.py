from pathlib import Path

from services.extraction_service import (
    ExtractionService,
)


TEST_FILE = Path(
    "temp/filing_text.txt"
)


def main() -> None:
    print("=" * 60)
    print("SEC Extraction Service Test")
    print("=" * 60)

    if not TEST_FILE.exists():
        print(
            f"Test file not found: {TEST_FILE}"
        )
        return

    service = ExtractionService()

    company = service.extract_from_text_file(
        TEST_FILE,
        accession_number="0001104659-26-090033",
        cik="0000874716",
    )

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
    print("EXTRACTION SERVICE TEST: PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()