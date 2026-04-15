import requests
import pytest


@pytest.mark.integration
def test_health_endpoint_available(base_url: str) -> None:
    response = requests.get(f"{base_url.rstrip('/')}/health", timeout=5)
    assert response.status_code == 200
    body = response.json()
    assert body.get("status") in {"ok", "healthy"}
