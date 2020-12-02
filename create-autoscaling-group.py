import boto3

client = boto3.client('autoscaling', region_name='us-west-2')

user_data = """#!/bin/bash
cd /tasks
./run.sh
"""

oregon_client = boto3.client('ec2', region_name='us-west-2')

# Pega o image id pelo nome da imagem
images = oregon_client.describe_images(
    Filters=[{'Name': 'name', 'Values': ['ami-daher']}])['Images']
if len(images) == 1:
    imageId = images[0]['ImageId']
    print("Using image", imageId)

# Pega o grupo id pelo nome do security group
groups = oregon_client.describe_security_groups(
    Filters=[{'Name': 'group-name', 'Values': ['SSH-DJANGO']}])['SecurityGroups']
if len(groups) == 1:
    groupId = groups[0]['GroupId']
    print("Using security group", groupId)

launchConfig = client.create_launch_configuration(
    LaunchConfigurationName='launch-config-daher',
    ImageId=imageId,
    KeyName='daher-key',
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

# Conecta as intancias do autoscaling group ao loadbalancer
response = client.attach_load_balancers(
    AutoScalingGroupName='auto-scaling-group-daher',
    LoadBalancerNames=['loadbalancer-daher']
)

print("Script finalizado!")
