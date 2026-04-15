from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class RunConfig:
    base_url: str
    reports_dir: Path


def run_pytest(config: RunConfig) -> int:
    config.reports_dir.mkdir(parents=True, exist_ok=True)
    junit_path = config.reports_dir / "junit.xml"
    command = [
        "pytest",
        "-q",
        f"--junitxml={junit_path}",
        f"--base-url={config.base_url}",
    ]
    return subprocess.run(command, check=False).returncode


def main() -> int:
    config = RunConfig(base_url="http://localhost:8000", reports_dir=Path("artifacts"))
    return run_pytest(config)


if __name__ == "__main__":
    raise SystemExit(main())
