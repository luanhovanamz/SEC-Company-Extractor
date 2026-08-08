from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Executive:
    """Information about a company executive."""

    name: str = ""
    title: str = ""


@dataclass
class Company:
    """Structured company information extracted from an SEC filing."""

    company_name: str = ""

    cik: str = ""
    accession_number: str = ""

    state_of_incorporation: str = ""
    commission_file_number: str = ""

    employer_identification_number: str = ""

    business_address: str = ""
    city: str = ""
    state: str = ""
    zip_code: str = ""

    phone: str = ""

    mailing_address: str = ""

    president: str = ""
    ceo: str = ""

    executives: list[Executive] = field(
        default_factory=list
    )

    source_filing: str = ""