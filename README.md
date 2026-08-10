# AWS Python SDK Scripts

Six short, standalone Python scripts using boto3 for basic AWS tasks: EC2 volume snapshots and simple S3 operations. These are reference snippets, not a library or CLI tool — no argument parsing, no config file, no tests.

## ⚠️ Known issues (2026-08-10)

- **`Backup_running_instances.py`** and **`aws_s3_list_buckets.py`** use Python 2 syntax (`filter(...)[0]` indexing and a bare `print` statement respectively) and will raise errors under Python 3. They have not been ported.
- None of the scripts take command-line arguments, read a config file, or have a test suite. Every "parameter" (bucket name, file path, region) is hardcoded in the script and must be edited by hand before running.
- Read each script before running it — none of them prompt for confirmation before creating snapshots or touching S3 objects.

## Contents

### EC2 Backup Scripts

#### **Backup_all_volumes.py**
9 lines. Iterates every EBS volume visible to the configured credentials and calls `create_snapshot()` on each one, tagged with the volume ID in the description. No region loop, no tag-based filtering, no retention/cleanup logic — it snapshots everything, every time it runs.

#### **Backup_running_instances.py**
17 lines. Filters EC2 instances to `running` state, then snapshots each attached volume. Uses Python 2-style `filter(...)[0]` list indexing on the instance's tags, which raises `TypeError` under Python 3 (`filter()` returns an iterator, not a list). Needs a small fix (`list(filter(...))[0]` or a generator expression) before it will run on modern Python.

#### **Complete_backup_script.py**
A short script combining instance and volume enumeration into one pass. No CLI flags, no cron/EventBridge wiring, no notification integration, and no rollback logic — "complete" refers to covering both instances and volumes in one file, not to feature completeness.

### S3 Scripts

#### **aws_s3_copy_bucket_to_bucket.py**
Copies objects from one S3 bucket to another using the bucket/key names hardcoded at the top of the file. No retry logic, no cross-region handling beyond whatever boto3 does by default, no progress reporting.

#### **aws_s3_list_buckets.py**
Lists all buckets and, for each one, all object keys. Uses a Python 2 `print` statement that raises `SyntaxError` under Python 3 — needs `print(...)` parens added before it will run. No size/cost/permission analysis.

#### **aws_s3_uploadfile.py**
Uploads a single hardcoded local file to a hardcoded bucket/key. No encryption flag, no content-type detection, no batch mode.

## 🚀 Usage

### Prerequisites
```bash
# Install boto3
pip install boto3

# Configure AWS credentials
aws configure
# Or use IAM roles for EC2 instances
```

### Running a script

Each script has its target (bucket name, file path, etc.) hardcoded near the top — open the file, edit those values, then run it directly:

```bash
python Backup_all_volumes.py
python Backup_running_instances.py   # fix the Python 3 filter() issue first, see Known issues above
python Complete_backup_script.py
python aws_s3_copy_bucket_to_bucket.py
python aws_s3_list_buckets.py        # fix the Python 3 print statement first, see Known issues above
python aws_s3_uploadfile.py
```

There are no `--region`, `--retention-days`, `--tag`, or similar flags on any script in this repo today — editing the source is the interface.

## 🔧 Configuration

### AWS Credentials Setup

**Option 1: AWS CLI**
```bash
aws configure
```

**Option 2: Environment Variables**
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

**Option 3: IAM Role (Recommended for EC2)**

Attach an IAM role to the EC2 instance running these scripts — no credentials needed in code.

### Required IAM Permissions

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:DescribeVolumes",
        "ec2:CreateSnapshot",
        "ec2:DescribeSnapshots"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket",
        "s3:GetObject",
        "s3:PutObject",
        "s3:CopyObject"
      ],
      "Resource": "arn:aws:s3:::*"
    }
  ]
}
```

## ⚠️ Important Notes

### Cost Considerations
- **EBS snapshots** incur storage costs in AWS — `Backup_all_volumes.py` snapshots every volume with no cleanup, so cost grows unbounded if run repeatedly without manual snapshot deletion.
- **S3 storage** costs based on total size and retrieval frequency.

### Security Best Practices
- **Use IAM roles** instead of access keys when possible.
- **Enable MFA** for AWS account access.
- **Principle of least privilege** for IAM permissions — the policy above is broader than any single script needs; scope it down per script if used in production.

## 📚 Related Resources

- **Misc_Ansible_Playbooks**: General Ansible automation playbooks
- **ansible**: System administration playbooks

## 🤝 Contributing

Contributions welcome! Please:
1. Fix the two Python 3 compatibility issues noted above
2. Add basic error handling and argument parsing if you extend these
3. Test in non-production AWS accounts first

## 📝 License

AWS automation scripts - Free to use and modify.

---
**AWS Python SDK Scripts** - Six small, hardcoded boto3 reference snippets. Read before running.
