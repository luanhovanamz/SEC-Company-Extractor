from sec.http_client import HttpClient
from sec.filing_downloader import FilingDownloader


def main() -> None:
    http = HttpClient(
        user_agent="SEC Company Extractor (luanhovanamz@gmail.com)"
    )

    try:
        downloader = FilingDownloader(http)

        file_path = downloader.download(
            cik="0000874716",
            accession_number="0001104659-26-090033",
            primary_document="tm2622041d1_8k.htm",
        )

        print("=" * 70)
        print("SEC Filing Download Test")
        print("=" * 70)

        print("Downloaded:", file_path)

        print("=" * 70)

    finally:
        http.close()


if __name__ == "__main__":
    main()