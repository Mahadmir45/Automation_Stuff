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
3. Run fast unit tests: `pytest -m "not integration"`.
4. Run full suite against target: `python src/embedded_test_automation/runner.py --base-url http://target-ip:8000`.
5. Build docs with `sphinx-build -b html docs docs/_build`.

## What This Starter Includes

- `src/embedded_test_automation/runner.py`: CLI-enabled test execution orchestrator with timeout controls
- `tests/test_health_endpoint.py`: sample API smoke test
- `tests/test_runner.py`: command construction unit test
- `docs/index.rst`: docs scaffold with doctest support

## Production Extensions

- device lab execution matrix by firmware/version
- signed test evidence and immutable storage
- Confluence publish via API token and space/page routing
