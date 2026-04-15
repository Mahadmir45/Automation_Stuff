from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Event:
    source: str
    event_type: str
    payload: dict


def route_event(event: Event) -> str:
    if event.source == "n8n" and event.event_type == "provisioning_request":
        return "infra-self-service-portal"
    if event.source == "aws" and event.event_type == "compliance_alert":
        return "cloud-governance-suite"
    return "dead-letter"
