# Cloud Governance Automation Suite

Automates AWS compliance checks and reporting for security and cost governance.

## Checks Included

- security groups open to world
- EC2 instances with more than one EBS volume
- resources missing required cost tags

## Stack

- Python 3.11+
- boto3

## Run

```bash
python src/cloud_governance_suite/audit.py
```
