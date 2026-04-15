from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

import boto3


def get_open_security_groups(ec2: Any) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    paginator = ec2.get_paginator("describe_security_groups")
    for page in paginator.paginate():
        for sg in page.get("SecurityGroups", []):
            for permission in sg.get("IpPermissions", []):
                for ip_range in permission.get("IpRanges", []):
                    if ip_range.get("CidrIp") == "0.0.0.0/0":
                        findings.append(
                            {
                                "security_group_id": sg["GroupId"],
                                "security_group_name": sg["GroupName"],
                                "port": str(permission.get("FromPort", "all")),
                                "protocol": str(permission.get("IpProtocol", "all")),
                            }
                        )
    return findings


def get_instances_with_multiple_disks(ec2: Any) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    paginator = ec2.get_paginator("describe_instances")
    for page in paginator.paginate():
        for reservation in page.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                volume_count = len(instance.get("BlockDeviceMappings", []))
                if volume_count > 1:
                    findings.append(
                        {
                            "instance_id": instance["InstanceId"],
                            "volume_count": str(volume_count),
                            "state": instance.get("State", {}).get("Name", "unknown"),
                        }
                    )
    return findings


def get_resources_missing_cost_tag(ec2: Any, required_cost_tag: str) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    paginator = ec2.get_paginator("describe_instances")
    for page in paginator.paginate():
        for reservation in page.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                tags = {tag["Key"]: tag["Value"] for tag in instance.get("Tags", [])}
                if required_cost_tag not in tags:
                    findings.append(
                        {
                            "instance_id": instance["InstanceId"],
                            "missing_tag": required_cost_tag,
                            "state": instance.get("State", {}).get("Name", "unknown"),
                        }
                    )
    return findings


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run AWS governance checks.")
    parser.add_argument("--region", default="us-east-1", help="AWS region for EC2 client.")
    parser.add_argument(
        "--reports-dir",
        default="reports",
        help="Directory where governance reports are written.",
    )
    parser.add_argument(
        "--required-cost-tag",
        default="cost_code",
        help="Required EC2 tag key used for cost attribution.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    reports_dir = Path(args.reports_dir)
    ec2 = boto3.client("ec2", region_name=args.region)

    open_sgs = get_open_security_groups(ec2)
    multi_disk_instances = get_instances_with_multiple_disks(ec2)
    missing_cost_tags = get_resources_missing_cost_tag(ec2, args.required_cost_tag)

    write_csv(reports_dir / "open_security_groups.csv", open_sgs)
    write_csv(reports_dir / "instances_with_multiple_disks.csv", multi_disk_instances)
    write_csv(reports_dir / "instances_missing_cost_tag.csv", missing_cost_tags)

    summary = {
        "region": args.region,
        "checks": {
            "open_security_groups": len(open_sgs),
            "instances_with_multiple_disks": len(multi_disk_instances),
            "instances_missing_cost_tag": len(missing_cost_tags),
        },
    }
    write_json(reports_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
