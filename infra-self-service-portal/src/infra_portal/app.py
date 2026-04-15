from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/requests":
            self.send_response(404)
            self.end_headers()
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(content_length))

        required_tags = {"owner", "cost_code", "environment"}
        missing = sorted(required_tags - payload.get("tags", {}).keys())

        if missing:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({"missing_tags": missing}).encode("utf-8"))
            return

        response = {
            "status": "accepted",
            "message": "Provisioning request validated and queued.",
        }
        self.send_response(202)
        self.end_headers()
        self.wfile.write(json.dumps(response).encode("utf-8"))


def main() -> None:
    server = HTTPServer(("127.0.0.1", 8081), RequestHandler)
    print("Serving infra self-service API on http://127.0.0.1:8081")
    server.serve_forever()


if __name__ == "__main__":
    main()
