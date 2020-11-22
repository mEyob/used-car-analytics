import boto3
from datetime import datetime
region = 'us-east-1'
ec2 = boto3.resource('ec2', region_name=region)


def lambda_handler(event, context):
    action = event.get("action") or ""

    if action == "stop":
        ec2.instances.filter(Filters=[{
            'Name': "tag:Name",
            'Values': ["scrapper"]
        }]).stop()
        current_time = datetime.utcnow().strftime("%Y-%m-%d %H-%M-%S")
        print(f'Stopped scrapper instance at {current_time}')
    else:
        ec2.instances.filter(Filters=[{
            'Name': "tag:Name",
            'Values': ["scrapper"]
        }]).start()
        current_time = datetime.utcnow().strftime("%Y-%m-%d %H-%M-%S")
        print(f'Started scrapper instance at {current_time}')
