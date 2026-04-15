import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--base-url", action="store", default="http://localhost:8000")


@pytest.fixture
def base_url(pytestconfig: pytest.Config) -> str:
    return str(pytestconfig.getoption("--base-url"))
