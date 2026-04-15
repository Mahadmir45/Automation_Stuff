from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass
class Event:
    source: str
    event_type: str
    payload: dict[str, object]


RouteHandler = Callable[[Event], str]


def default_dead_letter_handler(_: Event) -> str:
    return "dead-letter"


def build_route_table() -> dict[tuple[str, str], str]:
    return {
        ("n8n", "provisioning_request"): "infra-self-service-portal",
        ("aws", "compliance_alert"): "cloud-governance-suite",
        ("monitoring", "incident_created"): "incident-response-workflow",
    }


def route_event(event: Event, dead_letter_handler: RouteHandler = default_dead_letter_handler) -> str:
    route_table = build_route_table()
    destination = route_table.get((event.source, event.event_type))
    if destination:
        return destination
    return dead_letter_handler(event)
