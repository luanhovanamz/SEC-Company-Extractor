from __future__ import annotations

import time
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class HttpClient:
    """Shared HTTP client for SEC requests."""

    def __init__(
        self,
        user_agent: str,
        timeout: int = 30,
        delay: float = 0.2,
    ) -> None:

        self._timeout = timeout
        self._delay = delay

        self._session = requests.Session()

        retry = Retry(
            total=3,
            connect=3,
            read=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )

        adapter = HTTPAdapter(max_retries=retry)

        self._session.mount("https://", adapter)
        self._session.mount("http://", adapter)

        self._session.headers.update(
            {
                "User-Agent": user_agent,
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
            }
        )

    def get(
        self,
        url: str,
        params: dict[str, Any] | None = None,
    ) -> requests.Response:

        time.sleep(self._delay)

        response = self._session.get(
            url=url,
            params=params,
            timeout=self._timeout,
        )

        response.raise_for_status()

        return response

    def close(self) -> None:
        self._session.close()