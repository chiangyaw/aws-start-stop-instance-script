import boto3

def start_instances():
    tag_key = 'StopInstance'
    tag_value = 'True'
    
    ec2 = boto3.client('ec2')
    
    # Describe instances with the tag key and value
    response = ec2.describe_instances(
            Filters=[
                {
                    'Name': 'tag:{0}'.format(tag_key),
                    'Values': [tag_value]
                },
                {
                    'Name': 'instance-state-name',
                    'Values': ['stopped']
                }
            ]
        )
    
    # Collect all instance IDs
    instance_ids = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_ids.append(instance['InstanceId'])
            
    if instance_ids:
        ec2.start_instances(InstanceIds=instance_ids)
        ec2.delete_tags(
                Resources=instance_ids,
                Tags=[{'Key': tag_key}]
            )
    else:
        return f"No instance to start"
        
    return f"Instances started successfully"
    

def lambda_handler(event, context):
    result = start_instances()
    return {
        'statusCode': 200,
        'body': (result)
    }
