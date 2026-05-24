# AWS Python SDK Scripts

Collection of Python scripts using AWS SDK (boto3) for common AWS infrastructure tasks including EC2 backup automation, S3 operations, and instance management.

## 🎯 Overview

This repository contains Python automation scripts for AWS cloud infrastructure management using boto3. Each script is designed to be standalone, reusable, and production-ready for common DevOps tasks.

## 📁 Contents

### EC2 Backup Scripts

#### **Backup_all_volumes.py**
Automated backup solution for all EC2 volumes in an account:
- **Discovers all EC2 volumes** across regions
- **Creates snapshots** with descriptive tags
- **Automated cleanup** of old snapshots based on retention policies
- **Progress tracking** and error handling
- **Cost optimization** by removing outdated backups

#### **Backup_running_instances.py**
Targeted backup for active EC2 instances:
- **Identifies running instances** only (skip stopped ones)
- **Instance-aware backups** - preserves instance context
- **Tag-based organization** for easy restoration
- **Multi-region support** for distributed applications

#### **Complete_backup_script.py**
Comprehensive backup automation combining all features:
- **Full infrastructure backup** - instances, volumes, and configurations
- **Scheduled execution** support via cron/EventBridge
- **Notification integration** for backup status
- **Rollback capabilities** with snapshot restoration
- **Logging and monitoring** for audit trails

### S3 Management Scripts

#### **aws_s3_copy_bucket_to_bucket.py**
S3 bucket-to-bucket data replication:
- **Cross-region replication** automation
- **Incremental copying** for efficiency
- **Metadata preservation** during transfer
- **Error handling** and retry logic
- **Progress reporting** for large transfers

#### **aws_s3_list_buckets.py**
S3 inventory and management:
- **Bucket discovery** across all regions
- **Size analysis** and cost estimation
- **Permission auditing** for security compliance
- **Lifecycle rule** review and optimization

#### **aws_s3_uploadfile.py**
Simplified S3 file upload utility:
- **Single file upload** with proper permissions
- **Content-type detection** for web serving
- **Encryption support** (SSE-S3, SSE-KMS)
- **Public/private access** control
- **Batch upload** capability

## 🚀 Usage

### Prerequisites
```bash
# Install boto3 and dependencies
pip install boto3

# Configure AWS credentials
aws configure
# Or use IAM roles for EC2 instances
```

### EC2 Backup Examples

#### Backup All Volumes
```bash
# Backup all volumes with default retention
python Backup_all_volumes.py

# Specify region and retention days
python Backup_all_volumes.py --region us-east-1 --retention-days 30

# Tag-based backup
python Backup_all_volumes.py --tag Environment=Production --retention-days 90
```

#### Backup Running Instances Only
```bash
# Backup only running instances (cost-effective)
python Backup_running_instances.py

# Backup specific instance types
python Backup_running_instances.py --instance-types t3.micro,t3.small

# Exclude instances by tag
python Backup_running_instances.py --exclude-tag BackupDisabled=true
```

#### Complete Backup Strategy
```bash
# Full infrastructure backup
python Complete_backup_script.py --full

# Incremental backup (last 24 hours only)
python Complete_backup_script.py --incremental

# Scheduled backup (for cron)
python Complete_backup_script.py --scheduled --notify-email admin@example.com
```

### S3 Operations

#### Bucket Replication
```bash
# Copy entire bucket to another region
python aws_s3_copy_bucket_to_bucket.py --source my-bucket --dest my-bucket-backup --dest-region us-west-2

# Verify after copy
python aws_s3_copy_bucket_to_bucket.py --source my-bucket --dest my-bucket-backup --verify-only
```

#### S3 Inventory
```bash
# List all buckets with sizes
python aws_s3_list_buckets.py --detailed

# Cost analysis
python aws_s3_list_buckets.py --cost-estimate

# Security audit
python aws_s3_list_buckets.py --audit-permissions
```

#### File Upload
```bash
# Upload single file
python aws_s3_uploadfile.py --bucket my-bucket --file document.pdf

# Upload with encryption
python aws_s3_uploadfile.py --bucket my-bucket --file secret.txt --encrypt

# Public upload for website hosting
python aws_s3_uploadfile.py --bucket my-bucket --file index.html --public
```

## 🔧 Configuration

### AWS Credentials Setup

**Option 1: AWS CLI**
```bash
aws configure
# Enter AWS Access Key ID
# Enter AWS Secret Access Key
# Enter default region (us-east-1)
```

**Option 2: Environment Variables**
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

**Option 3: IAM Role (Recommended for EC2)**
```bash
# Attach IAM role to EC2 instance with appropriate permissions
# No credentials needed in code
```

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
        "ec2:DeleteSnapshot",
        "ec2:CreateTags",
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
        "s3:CopyObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::*"
    }
  ]
}
```

## 📋 Script Features

### Backup Automation
- **Scheduled backups** via cron or AWS EventBridge
- **Retention policies** for automatic cleanup
- **Cost monitoring** and optimization
- **Multi-region disaster recovery**
- **Incremental backup support**

### S3 Management
- **Batch operations** for efficiency
- **Cross-region replication**
- **Encryption at rest** and in transit
- **Version control** integration
- **Lifecycle automation**

## 🛠️ Advanced Examples

### Disaster Recovery Setup
```bash
# Daily automated backup
0 2 * * * /usr/bin/python3 /path/to/Complete_backup_script.py --scheduled --notify-email ops@example.com

# Weekly cross-region replication
0 3 * * 0 /usr/bin/python3 /path/to/aws_s3_copy_bucket_to_bucket.py --source prod-bucket --dest dr-bucket --dest-region us-west-2
```

### Cost Optimization
```bash
# Find and delete old snapshots
python Backup_all_volumes.py --cleanup --retention-days 30

# Analyze S3 storage costs
python aws_s3_list_buckets.py --cost-estimate --sort-by-cost
```

## 🔍 Monitoring & Logging

### Backup Monitoring
```bash
# Enable detailed logging
python Complete_backup_script.py --log-level DEBUG --log-file /var/log/aws-backups.log

# CloudWatch integration
python Complete_backup_script.py --cloudwatch-metrics
```

### Error Handling
All scripts include:
- **Try-catch blocks** for AWS API errors
- **Retry logic** for transient failures
- **Graceful degradation** when services are unavailable
- **Detailed error messages** for troubleshooting

## ⚠️ Important Notes

### Cost Considerations
- **EBS snapshots** incur storage costs in AWS
- **Data transfer** costs apply to cross-region operations
- **S3 storage** costs based on total size and retrieval frequency
- **Monitor AWS billing** regularly when running these scripts

### Security Best Practices
- **Use IAM roles** instead of access keys when possible
- **Enable MFA** for AWS account access
- **Encrypt sensitive data** both in transit and at rest
- **Principle of least privilege** for IAM permissions
- **Rotate credentials** regularly

## 📚 Related Resources

- **SysAdmin-Shell-Scripts**: Linux system administration utilities
- **Misc_Ansible_Playbooks**: AWS infrastructure provisioning with Ansible
- **IAC**: Infrastructure as Code with Terraform and Pulumi

## 🤝 Contributing

Contributions welcome! Please:
1. Follow AWS SDK best practices
2. Include error handling and retry logic
3. Add documentation for new scripts
4. Test in non-production AWS accounts first

## 📝 License

AWS automation scripts - Free to use and modify.

---

**AWS Python SDK Scripts** - Automating cloud infrastructure management with reliable, production-ready Python scripts.
