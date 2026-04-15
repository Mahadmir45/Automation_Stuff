from __future__ import annotations

import argparse
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


@dataclass
class RunConfig:
    base_url: str
    reports_dir: Path
    test_path: str
    timeout_seconds: int


def build_pytest_command(config: RunConfig) -> list[str]:
    junit_path = config.reports_dir / "junit.xml"
    return [
        "pytest",
        config.test_path,
        "-q",
        f"--junitxml={junit_path}",
        f"--base-url={config.base_url}",
    ]


def run_pytest(config: RunConfig) -> int:
    config.reports_dir.mkdir(parents=True, exist_ok=True)
    command = build_pytest_command(config)
    try:
        completed = subprocess.run(command, check=False, timeout=config.timeout_seconds)
        return completed.returncode
    except subprocess.TimeoutExpired:
        print(f"Test run timed out after {config.timeout_seconds} seconds.")
        return 124


def parse_args(argv: Sequence[str] | None = None) -> RunConfig:
    parser = argparse.ArgumentParser(description="Run embedded API tests with pytest.")
    parser.add_argument(
        "--base-url",
        default=os.getenv("BASE_URL", "http://localhost:8000"),
        help="Base URL for embedded system API.",
    )
    parser.add_argument(
        "--reports-dir",
        default=os.getenv("REPORTS_DIR", "artifacts"),
        help="Directory where test artifacts are written.",
    )
    parser.add_argument(
        "--test-path",
        default="tests",
        help="Path passed to pytest (directory, file, or node id).",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=600,
        help="Global timeout for pytest subprocess execution.",
    )
    args = parser.parse_args(argv)
    return RunConfig(
        base_url=args.base_url,
        reports_dir=Path(args.reports_dir),
        test_path=args.test_path,
        timeout_seconds=args.timeout_seconds,
    )


def main() -> int:
    config = parse_args()
    return run_pytest(config)


if __name__ == "__main__":
    raise SystemExit(main())
