from infra_portal.app import validate_request_payload


def test_validate_request_payload_accepts_valid_input() -> None:
    payload = {
        "request_name": "dev-app-server",
        "tags": {"owner": "devops", "cost_code": "ENG123", "environment": "dev"},
    }
    result = validate_request_payload(payload)
    assert result.valid is True
    assert result.errors == []


def test_validate_request_payload_rejects_missing_data() -> None:
    payload = {"request_name": "", "tags": {"owner": "devops"}}
    result = validate_request_payload(payload)
    assert result.valid is False
    assert len(result.errors) >= 1
