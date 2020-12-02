import boto3

# Get ohio instance public ip
ohio_client = boto3.client('ec2', region_name='us-east-2')
instances = ohio_client.describe_instances(Filters=[
    {'Name': 'tag:Name', 'Values': ['postgres-daher']},
    {'Name': 'instance-state-name', 'Values': ['running']}])['Reservations']
if len(instances) == 1:
    ohio_publicIP = instances[0]['Instances'][0]['PublicIpAddress']
print(ohio_publicIP)


client = boto3.client('autoscaling', region_name='us-west-2')

user_data = """#!/bin/bash
cd /tasks/portfolio
sed -i "s/node1/{0}/g" settings.py
cd /tasks
./run.sh
""".format(ohio_publicIP)

oregon_client = boto3.client('ec2', region_name='us-west-2')

images = oregon_client.describe_images(
    Filters=[{'Name': 'name', 'Values': ['ami-daher']}])['Images']
if len(images) == 1:
    imageId = images[0]['ImageId']
    print("Using image", imageId)

groups = oregon_client.describe_security_groups(
    Filters=[{'Name': 'group-name', 'Values': ['SSH-DJANGO']}])['SecurityGroups']
if len(groups) == 1:
    groupId = groups[0]['GroupId']
    print("Using security group", groupId)

launchConfig = client.create_launch_configuration(
    LaunchConfigurationName='launch-config-daher',
    ImageId=imageId,
    SecurityGroups=[groupId],
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
