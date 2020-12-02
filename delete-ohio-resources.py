import boto3

client = boto3.client('ec2', region_name='us-east-2')

instances = client.describe_instances(Filters=[
    {'Name': 'tag:Name', 'Values': ['postgres-daher']},
    {'Name': 'instance-state-name', 'Values': ['running']}])['Reservations']

if len(instances) == 1:
    instanceId = instances[0]['Instances'][0]['InstanceId']
    waiter = client.get_waiter('instance_terminated')
    client.terminate_instances(InstanceIds=[instanceId])
    waiter.wait(Filters=[{'Name': 'tag:Name', 'Values': ['postgres-daher']}])
    print('Instance terminated.')

groups = client.describe_security_groups(Filters=[{'Name': 'group-name', 'Values': ['SSH-PG']}])['SecurityGroups']
if len(groups) == 1:
    client.delete_security_group(GroupName='SSH-PG')

print('No resources.')
