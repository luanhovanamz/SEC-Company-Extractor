from pathlib import Path

# =====================================================
# Application
# =====================================================

APP_NAME = "SEC Company Extractor Professional"
APP_VERSION = "0.1.0"

# =====================================================
# Directories
# =====================================================

ROOT_DIR = Path(__file__).parent

CACHE_DIR = ROOT_DIR / "cache"
OUTPUT_DIR = ROOT_DIR / "output"
LOG_DIR = ROOT_DIR / "logs"
RESOURCE_DIR = ROOT_DIR / "resources"

# =====================================================
# SEC
# =====================================================

SEC_BASE_URL = "https://www.sec.gov"

SEARCH_API = "https://efts.sec.gov/LATEST/search-index"

USER_AGENT = (
    "SEC Company Extractor "
    "(contact: your_email@example.com)"
)

REQUEST_TIMEOUT = 30

MAX_RETRY = 3
