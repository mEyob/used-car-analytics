import sys
import boto3
import logging
from datetime import datetime

ec2 = boto3.client("ec2", region_name="us-east-1")
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """
    """
    response = ec2.describe_instances(Filters=[{
        "Name": "tag:Name",
        "Values": ["scrapper"]
    }])
    try:
        instances = response.get("Reservations")[0].get("Instances")
    except:
        sys.exit("Unable to retrieve instances' details")

    instances_to_stop = []
    instances_to_start = []
    for instance in instances:
        state = instance.get("State").get("Name")
        instance_id = instance.get("InstanceId")
        if state.lower() == "running":
            instances_to_stop.append(instance_id)
        elif state.lower() == "stopped":
            instances_to_start.append(instance_id)

    if instances_to_start:
        ec2.start_instances(InstanceIds=instances_to_start)
        current_time = datetime.utcnow().strftime("%Y-%m-%d %H-%M-%S")
        logger.info(
            f'Started instances {instances_to_start} at {current_time}')
    if instances_to_stop:
        ec2.stop_instances(InstanceIds=instances_to_stop)
        current_time = datetime.utcnow().strftime("%Y-%m-%d %H-%M-%S")
        logger.info(
            f'Stopped instances {instances_to_start} at {current_time}')
