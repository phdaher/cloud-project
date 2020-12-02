import boto3

client = boto3.client('ec2', region_name='us-east-2')

instances = client.describe_instances(Filters=[
    {'Name': 'tag:Name', 'Values': ['postgres-daher']},
    {'Name': 'instance-state-name', 'Values': ['running']}])
instanceId = instances['Reservations'][0]['Instances'][0]['InstanceId']

waiter = client.get_waiter('instance_terminated')
client.terminate_instances(InstanceIds=[instanceId])
waiter.wait(Filters=[{'Name': 'tag:Name', 'Values': ['postgres-daher']}])
print('Instance terminated.')

print('No resources.')
