from sec.company_extractor import CompanyExtractor


def main() -> None:
    print("=" * 60)
    print("SEC Company Extractor Regression Test")
    print("=" * 60)

    extractor = CompanyExtractor.from_file(
        "temp/filing_text.txt",
        source_filing="tm2622041d1_8k.htm",
    )

    company = extractor.extract()

    print()
    print("Company name:")
    print(company.company_name)

    print()
    print("State of incorporation:")
    print(company.state_of_incorporation)

    print()
    print("Commission File Number:")
    print(company.commission_file_number)

    print()
    print("IRS Employer Identification Number:")
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
    print(company.president or "(not found)")

    print()
    print("CEO:")
    print(company.ceo or "(not found)")

    print()
    print("Executives:")

    for executive in company.executives:
        print(
            f"- {executive.name} | "
            f"{executive.title}"
        )

    print()
    print("=" * 60)

    # --------------------------------------------------
    # Regression assertions
    # --------------------------------------------------

    assert (
        company.company_name
        == "IDEXX LABORATORIES, INC."
    )

    assert (
        company.state_of_incorporation
        == "Delaware"
    )

    assert (
        company.commission_file_number
        == "000-19271"
    )

    assert (
        company.employer_identification_number
        == "01-0393723"
    )

    assert (
        company.business_address
        == "One IDEXX Drive"
    )

    assert company.city == "Westbrook"

    assert company.state == "Maine"

    assert company.zip_code == "04092"

    assert company.phone == "207.556.0300"

    assert company.president == ""

    assert company.ceo == ""

    assert len(company.executives) == 1

    assert (
        company.executives[0].name
        == "Andrew Emerson"
    )

    assert (
        company.executives[0].title
        == (
            "Executive Vice President, "
            "Chief Financial Officer and Treasurer"
        )
    )

    print()
    print("REGRESSION TEST: PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()