from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Filing:
    """Represents one SEC EDGAR filing."""

    accession_number: str
    cik: str
    company_name: str
    form: str
    filing_date: str
    business_state: str
    business_location: str
    primary_document: str