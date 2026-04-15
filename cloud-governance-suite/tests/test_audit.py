from cloud_governance_suite.audit import (
    get_instances_with_multiple_disks,
    get_open_security_groups,
    get_resources_missing_cost_tag,
)


class FakePaginator:
    def __init__(self, pages):
        self._pages = pages

    def paginate(self):
        return self._pages


class FakeEC2Client:
    def __init__(self, pages_by_name):
        self._pages_by_name = pages_by_name

    def get_paginator(self, name):
        return FakePaginator(self._pages_by_name[name])


def test_get_open_security_groups_detects_world_open_rule() -> None:
    ec2 = FakeEC2Client(
        {
            "describe_security_groups": [
                {
                    "SecurityGroups": [
                        {
                            "GroupId": "sg-1",
                            "GroupName": "public",
                            "IpPermissions": [
                                {"FromPort": 22, "IpProtocol": "tcp", "IpRanges": [{"CidrIp": "0.0.0.0/0"}]}
                            ],
                        }
                    ]
                }
            ]
        }
    )
    findings = get_open_security_groups(ec2)
    assert len(findings) == 1
    assert findings[0]["security_group_id"] == "sg-1"


def test_instance_checks_find_expected_violations() -> None:
    reservations = [
        {
            "Reservations": [
                {
                    "Instances": [
                        {
                            "InstanceId": "i-1",
                            "BlockDeviceMappings": [{"DeviceName": "/dev/xvda"}, {"DeviceName": "/dev/xvdb"}],
                            "State": {"Name": "running"},
                            "Tags": [{"Key": "owner", "Value": "platform"}],
                        },
                        {
                            "InstanceId": "i-2",
                            "BlockDeviceMappings": [{"DeviceName": "/dev/xvda"}],
                            "State": {"Name": "running"},
                            "Tags": [{"Key": "cost_code", "Value": "ENG42"}],
                        },
                    ]
                }
            ]
        }
    ]
    ec2 = FakeEC2Client({"describe_instances": reservations})

    multi_disk = get_instances_with_multiple_disks(ec2)
    missing_tag = get_resources_missing_cost_tag(ec2, "cost_code")

    assert [row["instance_id"] for row in multi_disk] == ["i-1"]
    assert [row["instance_id"] for row in missing_tag] == ["i-1"]
