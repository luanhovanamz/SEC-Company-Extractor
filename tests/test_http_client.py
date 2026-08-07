from sec.http_client import HttpClient


def main() -> None:
    client = HttpClient(
        user_agent="SEC Company Extractor (luanhovanamz@gmail.com)"
    )

    response = client.get("https://www.sec.gov")

    print(response.status_code)
    print(response.text[:200])

    client.close()


if __name__ == "__main__":
    main()