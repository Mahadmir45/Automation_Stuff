import requests


def test_health_endpoint_available(base_url: str) -> None:
    response = requests.get(f"{base_url}/health", timeout=5)
    assert response.status_code == 200
