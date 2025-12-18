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
