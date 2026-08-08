from __future__ import annotations

import re
from pathlib import Path

from models.company import Company, Executive


class CompanyExtractor:
    """
    Extract company information from cleaned SEC filing text.
    """

    US_STATES = {
        "Alabama",
        "Alaska",
        "Arizona",
        "Arkansas",
        "California",
        "Colorado",
        "Connecticut",
        "Delaware",
        "Florida",
        "Georgia",
        "Hawaii",
        "Idaho",
        "Illinois",
        "Indiana",
        "Iowa",
        "Kansas",
        "Kentucky",
        "Louisiana",
        "Maine",
        "Maryland",
        "Massachusetts",
        "Michigan",
        "Minnesota",
        "Mississippi",
        "Missouri",
        "Montana",
        "Nebraska",
        "Nevada",
        "New Hampshire",
        "New Jersey",
        "New Mexico",
        "New York",
        "North Carolina",
        "North Dakota",
        "Ohio",
        "Oklahoma",
        "Oregon",
        "Pennsylvania",
        "Rhode Island",
        "South Carolina",
        "South Dakota",
        "Tennessee",
        "Texas",
        "Utah",
        "Vermont",
        "Virginia",
        "Washington",
        "West Virginia",
        "Wisconsin",
        "Wyoming",
    }

    ADDRESS_STOP_WORDS = (
        "state or other jurisdiction",
        "commission file number",
        "irs employer identification",
        "exact name of registrant",
        "date of report",
        "current report",
        "pursuant to section",
        "of incorporation",
    )

    def __init__(
        self,
        text: str,
        source_filing: str = "",
    ) -> None:
        self._text = text

        self._lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        self._source_filing = source_filing

    @classmethod
    def from_file(
        cls,
        file_path: str | Path,
        source_filing: str = "",
    ) -> "CompanyExtractor":
        """Create extractor from a cleaned SEC text file."""

        path = Path(file_path)

        text = path.read_text(
            encoding="utf-8",
            errors="replace",
        )

        return cls(
            text=text,
            source_filing=source_filing or path.name,
        )

    @staticmethod
    def _normalize_label(value: str) -> str:
        """Normalize SEC labels."""

        value = value.strip().lower()

        value = value.replace("(", "")
        value = value.replace(")", "")
        value = value.replace(":", "")

        value = re.sub(
            r"\s+",
            " ",
            value,
        )

        return value.strip()

    @staticmethod
    def _digits(value: str) -> str:
        """Return only numeric characters."""

        return "".join(
            re.findall(r"\d", value)
        )

    def extract(self) -> Company:
        """Extract all supported company information."""

        company = Company(
            source_filing=self._source_filing
        )

        company.company_name = (
            self._extract_company_name()
        )

        company.state_of_incorporation = (
            self._extract_state_of_incorporation()
        )

        company.commission_file_number = (
            self._extract_commission_file_number()
        )

        company.employer_identification_number = (
            self._extract_ein()
        )

        (
            company.business_address,
            company.city,
            company.state,
            company.zip_code,
        ) = self._extract_address()

        company.phone = self._extract_phone()

        (
            company.president,
            company.ceo,
            company.executives,
        ) = self._extract_executives()

        return company

    def _find_label_index(
        self,
        label: str,
    ) -> int:
        """Find normalized label in SEC text."""

        target = self._normalize_label(
            label
        )

        for index, line in enumerate(
            self._lines
        ):
            normalized = self._normalize_label(
                line
            )

            if normalized == target:
                return index

        return -1

    def _extract_company_name(self) -> str:
        """Extract registrant name."""

        for index, line in enumerate(
            self._lines
        ):
            normalized = self._normalize_label(
                line
            )

            if (
                "exact name of registrant"
                in normalized
                and index > 0
            ):
                return self._lines[index - 1]

        return ""

    def _extract_state_of_incorporation(
        self,
    ) -> str:
        """Extract incorporation state."""

        for line in self._lines[:60]:
            candidate = line.strip()

            if candidate in self.US_STATES:
                return candidate

        return ""

    def _extract_commission_file_number(
        self,
    ) -> str:
        """Extract SEC Commission File Number."""

        header_text = "\n".join(
            self._lines[:60]
        )

        match = re.search(
            r"\b\d{3}-\d{4,6}\b",
            header_text,
        )

        if match:
            return match.group(0)

        return ""

    def _extract_ein(self) -> str:
        """Extract IRS Employer Identification Number."""

        match = re.search(
            r"\b\d{2}-\d{7}\b",
            self._text,
        )

        if match:
            return match.group(0)

        return ""

    def _is_address_stop_line(
        self,
        line: str,
    ) -> bool:
        """Return True if line belongs to SEC header metadata."""

        normalized = self._normalize_label(
            line
        )

        return any(
            word in normalized
            for word in self.ADDRESS_STOP_WORDS
        )

    def _extract_address(
        self,
    ) -> tuple[str, str, str, str]:
        """
        Extract principal executive office address.

        SEC cleaned text normally appears approximately as:

            One IDEXX Drive
            ,
            Westbrook
            ,
            Maine
            04092
            (Address of principal executive offices)

        The parser therefore identifies:

            State -> ZIP -> City -> Address
        """

        label_index = self._find_label_index(
            "Address of principal executive offices"
        )

        if label_index == -1:
            return "", "", "", ""

        # --------------------------------------------------
        # 1. Find the state immediately before the address
        #    label.
        # --------------------------------------------------

        state_index = -1

        search_start = label_index - 1
        search_end = max(
            -1,
            label_index - 15,
        )

        for index in range(
            search_start,
            search_end,
            -1,
        ):
            candidate = self._lines[index]

            if candidate in self.US_STATES:
                state_index = index
                break

        if state_index == -1:
            return "", "", "", ""

        state = self._lines[state_index]

        # --------------------------------------------------
        # 2. Find ZIP code after the state.
        # --------------------------------------------------

        zip_code = ""

        for index in range(
            state_index + 1,
            min(
                label_index,
                state_index + 6,
            ),
        ):
            candidate = self._lines[index]

            if re.fullmatch(
                r"\d{5}(?:-\d{4})?",
                candidate,
            ):
                zip_code = candidate
                break

        # --------------------------------------------------
        # 3. Find city immediately before the state.
        #
        # Skip punctuation lines such as "," and ".".
        # --------------------------------------------------

        city = ""
        city_index = -1

        for index in range(
            state_index - 1,
            max(
                -1,
                state_index - 6,
            ),
            -1,
        ):
            candidate = self._lines[index]

            if candidate in {
                ",",
                ".",
            }:
                continue

            if re.fullmatch(
                r"\d{5}(?:-\d{4})?",
                candidate,
            ):
                continue

            if self._is_address_stop_line(
                candidate
            ):
                break

            city = candidate
            city_index = index
            break

        if city_index == -1:
            return "", "", state, zip_code

        # --------------------------------------------------
        # 4. Everything immediately before the city is
        #    considered address, until an SEC header
        #    boundary is reached.
        # --------------------------------------------------

        address_parts = []

        for index in range(
            city_index - 1,
            -1,
            -1,
        ):
            candidate = self._lines[index]

            if candidate in {
                ",",
                ".",
            }:
                continue

            if self._is_address_stop_line(
                candidate
            ):
                break

            # Stop at another state.
            if candidate in self.US_STATES:
                break

            # Stop at obvious SEC metadata.
            normalized = self._normalize_label(
                candidate
            )

            if (
                "zip code" in normalized
                or "address of principal executive offices"
                in normalized
            ):
                break

            address_parts.insert(
                0,
                candidate,
            )

        business_address = " ".join(
            address_parts
        ).strip()

        return (
            business_address,
            city,
            state,
            zip_code,
        )

    def _extract_phone(self) -> str:
        """Extract registrant telephone number."""

        label_index = self._find_label_index(
            "Registrant's telephone number, including area code"
        )

        if label_index == -1:
            return ""

        start = max(
            0,
            label_index - 8,
        )

        candidates = self._lines[
            start:label_index
        ]

        groups = []

        for candidate in candidates:
            digits = self._digits(
                candidate
            )

            if digits:
                groups.append(digits)

        for index in range(
            len(groups) - 1
        ):
            first = groups[index]
            second = groups[index + 1]

            if (
                len(first) == 3
                and len(second) == 7
            ):
                return (
                    f"{first}."
                    f"{second[:3]}."
                    f"{second[3:]}"
                )

        combined = "".join(groups)

        if len(combined) >= 10:
            candidate = combined[-10:]

            return (
                f"{candidate[:3]}."
                f"{candidate[3:6]}."
                f"{candidate[6:]}"
            )

        return ""

    def _extract_executives(
        self,
    ) -> tuple[str, str, list[Executive]]:
        """
        Extract executives from SIGNATURES section.

        Do not infer President from:
            Executive Vice President
            Senior Vice President
            Vice President
        """

        executives: list[Executive] = []

        president = ""
        ceo = ""

        signature_index = (
            self._find_signature_index()
        )

        if signature_index == -1:
            return (
                president,
                ceo,
                executives,
            )

        section = self._lines[
            signature_index:
        ]

        for index, line in enumerate(
            section
        ):
            if not line.startswith("/s/"):
                continue

            name = line[3:].strip()

            next_index = index + 1

            if (
                next_index < len(section)
                and section[next_index].strip()
                == name
            ):
                next_index += 1

            if not name:
                if next_index < len(section):
                    name = section[
                        next_index
                    ].strip()

                    next_index += 1

            title_parts = []

            for position in range(
                next_index,
                min(
                    next_index + 5,
                    len(section),
                ),
            ):
                candidate = section[
                    position
                ].strip()

                if not candidate:
                    continue

                if candidate.startswith(
                    "/s/"
                ):
                    break

                if candidate in {
                    "1",
                    "2",
                    "3",
                    "4",
                }:
                    break

                if candidate.lower() in {
                    "signatures",
                    "by:",
                }:
                    continue

                title_parts.append(
                    candidate
                )

            title = " ".join(
                title_parts
            ).strip()

            if title and name:
                executive = Executive(
                    name=name,
                    title=title,
                )

                executives.append(
                    executive
                )

                title_lower = title.lower()

                if (
                    "chief executive officer"
                    in title_lower
                ):
                    ceo = name

                if re.search(
                    r"(?<!vice\s)"
                    r"\bpresident\b",
                    title_lower,
                ):
                    president = name

            break

        return (
            president,
            ceo,
            executives,
        )

    def _find_signature_index(self) -> int:
        """Find SIGNATURES section."""

        for index, line in enumerate(
            self._lines
        ):
            if (
                self._normalize_label(line)
                == "signatures"
            ):
                return index

        return -1