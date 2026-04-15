from __future__ import annotations

import argparse
import json
import uuid
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, HTTPServer


REQUIRED_TAGS = {"owner", "cost_code", "environment"}


@dataclass
class ValidationResult:
    valid: bool
    errors: list[str]


def validate_request_payload(payload: dict) -> ValidationResult:
    errors: list[str] = []

    request_name = payload.get("request_name")
    if not isinstance(request_name, str) or not request_name.strip():
        errors.append("request_name is required and must be a non-empty string")

    tags = payload.get("tags")
    if not isinstance(tags, dict):
        errors.append("tags is required and must be an object")
    else:
        missing = sorted(REQUIRED_TAGS - tags.keys())
        if missing:
            errors.append(f"missing required tags: {', '.join(missing)}")

    return ValidationResult(valid=not errors, errors=errors)


class RequestHandler(BaseHTTPRequestHandler):
    def _write_json(self, status_code: int, payload: dict) -> None:
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._write_json(200, {"status": "ok"})
            return
        self._write_json(404, {"error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/requests":
            self._write_json(404, {"error": "not found"})
            return

        request_id = str(uuid.uuid4())
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._write_json(400, {"request_id": request_id, "error": "invalid Content-Length"})
            return

        raw_payload = self.rfile.read(content_length)
        try:
            payload = json.loads(raw_payload.decode("utf-8"))
        except json.JSONDecodeError:
            self._write_json(400, {"request_id": request_id, "error": "invalid JSON payload"})
            return

        validation = validate_request_payload(payload)
        if not validation.valid:
            self._write_json(
                400,
                {"request_id": request_id, "status": "rejected", "errors": validation.errors},
            )
            return

        self._write_json(
            202,
            {
                "request_id": request_id,
                "status": "accepted",
                "message": "Provisioning request validated and queued.",
            },
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run infra self-service API server.")
    parser.add_argument("--host", default="127.0.0.1", help="Bind host for HTTP server.")
    parser.add_argument("--port", type=int, default=8081, help="Bind port for HTTP server.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    server = HTTPServer((args.host, args.port), RequestHandler)
    print(f"Serving infra self-service API on http://{args.host}:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
