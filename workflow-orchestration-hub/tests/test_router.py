from orchestration_hub.router import Event, route_event


def test_route_event_matches_known_routes() -> None:
    event = Event(source="n8n", event_type="provisioning_request", payload={})
    assert route_event(event) == "infra-self-service-portal"


def test_route_event_uses_dead_letter_handler() -> None:
    event = Event(source="custom", event_type="unknown", payload={})
    destination = route_event(event, dead_letter_handler=lambda _: "ops-review")
    assert destination == "ops-review"
