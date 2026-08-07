from config import APP_NAME, APP_VERSION


def main() -> None:
    print("=" * 50)
    print(APP_NAME)
    print(f"Version: {APP_VERSION}")
    print("=" * 50)


if __name__ == "__main__":
    main()
