from pathlib import Path

from services.config_service import ConfigService
from services.logger_service import LoggerService


def main() -> None:
    config = ConfigService(Path("data") / "settings.json")
    config.load()

    logger = LoggerService(Path("logs")).logger

    logger.info("Application started")

    print("=" * 60)
    print(config.get("application", "name"))
    print(f"Version : {config.get('application', 'version')}")
    print("=" * 60)

    logger.info("Configuration loaded successfully")

    print(f"SEC API : {config.get('sec', 'search_api')}")
    print(f"Threads : {config.get('worker', 'thread_count')}")

    logger.info("Application initialized successfully")


if __name__ == "__main__":
    main()