import boto3

client = boto3.client('ec2', region_name='us-west-2')

asg_client = boto3.client('autoscaling', region_name='us-west-2')

as_groups = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=['auto-scaling-group-daher'])['AutoScalingGroups']
if len(as_groups) == 1:
    asg_client.delete_auto_scaling_group(
        AutoScalingGroupName='auto-scaling-group-daher', ForceDelete=True)
    waiter = client.get_waiter('instance_terminated')
    waiter.wait(Filters=[{'Name': 'tag:Name', 'Values': ['django-daher']}])
    print('Instances terminated.')

launch_configs = asg_client.describe_launch_configurations(LaunchConfigurationNames=['launch-config-daher'])['LaunchConfigurations']
if len(launch_configs) == 1:
    asg_client.delete_launch_configuration(
        LaunchConfigurationName='launch-config-daher')


images = client.describe_images(
    Filters=[{'Name': 'name', 'Values': ['ami-daher']}])['Images']
if len(images) == 1:
    imageId = images[0]['ImageId']
    response = client.deregister_image(ImageId=imageId)

instances = client.describe_instances(Filters=[
    {'Name': 'tag:Name', 'Values': ['oregon-daher']},
    {'Name': 'instance-state-name', 'Values': ['running']}])['Reservations']

if len(instances) == 1:
    instanceId = instances[0]['Instances'][0]['InstanceId']
    waiter = client.get_waiter('instance_terminated')
    client.terminate_instances(InstanceIds=[instanceId])
    waiter.wait(Filters=[{'Name': 'tag:Name', 'Values': ['oregon-daher']}])
    print('Instance terminated.')

groups = client.describe_security_groups(
    Filters=[{'Name': 'group-name', 'Values': ['SSH-DJANGO']}])['SecurityGroups']
if len(groups) == 1:
    client.delete_security_group(GroupName='SSH-DJANGO')

print('No resources.')
