import boto3

def stop_and_tag_instances():
    ec2 = boto3.client('ec2')
    
    # Describe instances
    response = ec2.describe_instances(
        Filters=[

                {
                    'Name': 'instance-state-name',
                    'Values': ['running']
                }
            ]
        )
    
    # Collect all instance IDs
    instance_ids = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_ids.append(instance['InstanceId'])
    
    if not instance_ids:
        return f"No Instance found."
    
    # Stop instances
    ec2.stop_instances(InstanceIds=instance_ids)
    
    # Wait until all instances are stopped
    waiter = ec2.get_waiter('instance_stopped')
    waiter.wait(InstanceIds=instance_ids)
    
    # Tag instances
    ec2.create_tags(
        Resources=instance_ids,
        Tags=[{'Key': 'StopInstance', 'Value': 'True'}]
    )
    
    return f"Instances stopped and tagged."

def lambda_handler(event, context):
    result = stop_and_tag_instances()
    return {
        'statusCode': 200,
        'body': (result)
    }
