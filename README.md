# 🚀 Automated EC2 Instance Management with AWS Lambda & Boto3

## 📄 Overview
This project demonstrates how to automate the **starting and stopping of EC2 instances** using **AWS Lambda** and **Boto3**.  
Instances are managed based on tags:
- `Action=Auto-Stop` → stopped automatically.
- `Action=Auto-Start` → started automatically.

---

## 🛠️ Setup Steps

### 1. EC2 Instances
- Created two `t2.micro` instances (free tier).
- Tagged them:
  - **Instance 1** → `Name=kumarAuto-start`, `Action=Auto-Start`
  - **Instance 2** → `Name=kumarAuto-stop`, `Action=Auto-Stop`

📸 *Screenshot: EC2 dashboard showing both instances with tags.*

---

### 2. IAM Role
- Created IAM role: **`kumarlambdafun-role-jro4i8os`**
- Attached policies:
  - `AWSLambdaBasicExecutionRole` → for CloudWatch logging.
  - `AmazonEC2FullAccess` → for EC2 actions.

📸 *Screenshot: IAM role with attached policies.*

---

### 3. Lambda Function
- Runtime: **Python 3.x**
- Execution role: `kumarlambdafun-role-jro4i8os`
- Code:

```python
import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    # Stop instances tagged Auto-Stop
    stop_instances = ec2.describe_instances(
        Filters=[{'Name': 'tag:Action', 'Values': ['Auto-Stop']}]
    )
    stop_ids = [i['InstanceId'] for r in stop_instances['Reservations'] for i in r['Instances']]
    if stop_ids:
        ec2.stop_instances(InstanceIds=stop_ids)
        print(f"Stopped instances: {stop_ids}")

    # Start instances tagged Auto-Start
    start_instances = ec2.describe_instances(
        Filters=[{'Name': 'tag:Action', 'Values': ['Auto-Start']}]
    )
    start_ids = [i['InstanceId'] for r in start_instances['Reservations'] for i in r['Instances']]
    if start_ids:
        ec2.start_instances(InstanceIds=start_ids)
        print(f"Started instances: {start_ids}")

    return {
        "statusCode": 200,
        "body": f"Stopped: {stop_ids}, Started: {start_ids}"
    }
