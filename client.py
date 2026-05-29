import os
import uuid
from typing import Any

import requests

try:
    import local_config
except ImportError:
    local_config = None

SEAHOT_TOKEN = getattr(local_config, "SEAHOT_TOKEN", "")


BASE_URL = os.getenv("SEAHOT_BASE_URL", "https://aiart-openresty.dev.seaart.dev")
TOKEN = os.getenv("SEAHOT_TOKEN", SEAHOT_TOKEN)
USE_ENV_PROXY = os.getenv("SEAHOT_USE_ENV_PROXY", "0").lower() in {"1", "true", "yes", "on"}
REQUEST_TIMEOUT = float(os.getenv("SEAHOT_TIMEOUT", "15"))
REQUEST_RETRY = int(os.getenv("SEAHOT_RETRY", "2"))


def has_token() -> bool:
    return bool(TOKEN.strip())


class APIClient:
    def __init__(self, base_url: str = BASE_URL, token: str = TOKEN, timeout: float = REQUEST_TIMEOUT):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.timeout = timeout
        self.session = requests.Session()
        self.session.trust_env = USE_ENV_PROXY

    def post(self, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        url = path if path.startswith("http") else self.base_url + path
        last_error = None

        for _ in range(REQUEST_RETRY + 1):
            try:
                response = self.session.post(url, headers=self.headers(), json=body or {}, timeout=self.timeout)
                break
            except (requests.ConnectionError, requests.Timeout) as error:
                last_error = error
        else:
            raise AssertionError(f"请求失败: {url} - {last_error}")

        assert response.status_code == 200, response.text

        data = response.json()
        assert "status" in data, data
        assert "code" in data["status"], data
        assert data["status"]["code"] == 10000, data
        return data

    def headers(self) -> dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "X-Platform": "app",
            "X-App-Id": "app_global_seahot",
            "X-Device-Name": "Galaxy%20S24",
            "X-Device-OS": "Android",
            "X-Device-Model": "SM-S921U1",
            "X-Device-Sys-Version": "Android 16",
            "X-App-Version": "1.6.0.1779866239",
            "X-Device-Id": "python-demo-device",
            "X-Request-Id": str(uuid.uuid4()),
            "Accept-Language": "en",
            "X-Device-Language": "en",
            "User-Agent": "Mozilla/5.0 (Android 16) SeaHot/1.6.0.1779866239 SM-S921U1",
            "app_language": "zh-CN",
        }
        if self.token:
            headers["Token"] = self.token
        return headers
