# Infrastructure Self-Service Portal

Internal automation API that standardizes server build requests and triggers downstream provisioning pipelines.

## Features

- receives infra requests from dev teams
- validates tagging and environment rules
- prepares payloads for TeamCity/API-driven provisioning
- can be fronted by a simple web UI

## Run

```bash
python src/infra_portal/app.py
```
