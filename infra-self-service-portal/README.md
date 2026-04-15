# Infrastructure Self-Service Portal

Internal automation API that standardizes server build requests and triggers downstream provisioning pipelines.

## Features

- receives infra requests from dev teams
- validates tagging and environment rules
- prepares payloads for TeamCity/API-driven provisioning
- returns request IDs for traceability
- health endpoint for uptime checks (`/health`)

## Run

```bash
python src/infra_portal/app.py
```

Custom host/port:

```bash
python src/infra_portal/app.py --host 0.0.0.0 --port 8081
```
