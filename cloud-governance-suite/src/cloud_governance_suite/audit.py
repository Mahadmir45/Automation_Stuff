from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import boto3


def get_open_security_groups(ec2: Any) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    response = ec2.describe_security_groups()
    for sg in response.get("SecurityGroups", []):
        for permission in sg.get("IpPermissions", []):
            for ip_range in permission.get("IpRanges", []):
                if ip_range.get("CidrIp") == "0.0.0.0/0":
                    findings.append(
                        {
                            "security_group_id": sg["GroupId"],
                            "security_group_name": sg["GroupName"],
                            "port": str(permission.get("FromPort", "all")),
                        }
                    )
    return findings


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    ec2 = boto3.client("ec2")
    findings = get_open_security_groups(ec2)
    write_csv(Path("reports/open_security_groups.csv"), findings)
    print(f"Generated report with {len(findings)} findings.")


if __name__ == "__main__":
    main()
