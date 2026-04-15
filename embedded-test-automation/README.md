# Embedded Test Automation Platform

Automates embedded-system HTTP/API tests with `pytest`, generates technical docs with `Sphinx`, converts artifacts with `Pandoc`, and prepares content for Confluence publishing.

## Stack

- Python 3.11+
- pytest
- requests
- sphinx
- pandoc

## Quick Start

1. Create a virtual environment.
2. Install dependencies from `requirements.txt`.
3. Run `pytest`.
4. Build docs with `sphinx-build -b html docs docs/_build`.

## What This Starter Includes

- `src/embedded_test_automation/runner.py`: sample test execution orchestrator
- `tests/test_health_endpoint.py`: sample API smoke test
- `docs/index.rst`: docs scaffold with doctest support

## Production Extensions

- device lab execution matrix by firmware/version
- signed test evidence and immutable storage
- Confluence publish via API token and space/page routing
