import boto3

# Get ohio instance public ip
ohio_client = boto3.client('ec2', region_name='us-east-2')
instances = ohio_client.describe_instances(Filters=[
    {'Name': 'tag:Name', 'Values': ['postgres-daher']},
    {'Name': 'instance-state-name', 'Values': ['running']}])['Reservations']
if len(instances) == 1:
    ohio_publicIP = instances[0]['Instances'][0]['PublicIpAddress']
print(ohio_publicIP)
# -------

client = boto3.client('autoscaling', region_name='us-west-2')

user_data = """#!/bin/bash
cd /tasks/portfolio
sed ------------------
cd /tasks
./run.sh
"""

launchConfig = client.create_launch_configuration(
    LaunchConfigurationName='launch-config-daher',
    ImageId='ami-0acdb352a689a862f',
    KeyName='daher-key',
    SecurityGroups=['sg-0a2ccd80448aae5e0'],
    UserData=user_data,
    InstanceType='t2.micro',
    InstanceMonitoring={'Enabled': False},
    AssociatePublicIpAddress=True
)

autoScalingGroup = client.create_auto_scaling_group(
    AutoScalingGroupName='auto-scaling-group-daher',
    AvailabilityZones=['us-west-2a', 'us-west-2b', 'us-west-2c'],
    LaunchConfigurationName='launch-config-daher',
    MinSize=1,
    MaxSize=3,
    DesiredCapacity=3,
    DefaultCooldown=120,
    HealthCheckType='ELB',
    HealthCheckGracePeriod=60,
    Tags=[{'Key': 'Name', 'Value': 'django-daher'}],
)

response = client.attach_load_balancers(
    AutoScalingGroupName='auto-scaling-group-daher',
    LoadBalancerNames=['loadbalancer-daher']
)

print(response)
