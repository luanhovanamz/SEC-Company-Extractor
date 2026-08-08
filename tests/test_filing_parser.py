from pathlib import Path

from services.filing_parser import FilingParser


def main() -> None:
    filing_path = Path(
        "cache/tm2622041d1_8k.htm"
    )

    print("=" * 70)
    print("SEC Filing Parser Test")
    print("=" * 70)

    if not filing_path.exists():
        print(
            "ERROR: Filing file does not exist:"
        )
        print(filing_path)
        print()
        print(
            "Run the filing downloader test first."
        )
        return

    parser = FilingParser(filing_path)

    html = parser.read_html()

    print(
        "HTML size:",
        len(html),
        "characters",
    )

    text = parser.get_text()

    print(
        "Clean text size:",
        len(text),
        "characters",
    )

    output = parser.save_text(
        "temp/filing_text.txt"
    )

    print(
        "Clean text saved:",
        output,
    )

    print("\nFirst 30 lines:")
    print("-" * 70)

    lines = text.splitlines()

    for line in lines[:30]:
        print(line)

    print("=" * 70)


if __name__ == "__main__":
    main()