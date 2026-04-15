from pathlib import Path

from embedded_test_automation.runner import RunConfig, build_pytest_command


def test_build_pytest_command_contains_expected_arguments() -> None:
    config = RunConfig(
        base_url="http://device.local:8080",
        reports_dir=Path("artifacts"),
        test_path="tests/test_health_endpoint.py",
        timeout_seconds=300,
    )

    command = build_pytest_command(config)

    assert command[0] == "pytest"
    assert "--base-url=http://device.local:8080" in command
    assert "--junitxml=artifacts/junit.xml" in command
