import boto3

asg_client = boto3.client('autoscaling', region_name='us-west-2')
elb_client = boto3.client('elb', region_name='us-west-2')

if len(asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=['auto-scaling-group-daher'])['AutoScalingGroups']) > 0:
    asg_client.delete_auto_scaling_group(
        AutoScalingGroupName='auto-scaling-group-daher', ForceDelete=True)

if len(asg_client.describe_launch_configurations(LaunchConfigurationNames=['launch-config-daher'])['LaunchConfigurations']) > 0:
    asg_client.delete_launch_configuration(
        LaunchConfigurationName='launch-config-daher')

if len(elb_client.describe_load_balancers()['LoadBalancerDescriptions']) > 0:
    elb_client.delete_load_balancer(
        LoadBalancerName='loadbalancer-daher')

print('No resources.')
