import boto3

elb_client = boto3.client('elb', region_name='us-west-2')

if len(elb_client.describe_load_balancers()['LoadBalancerDescriptions']) > 0:
    elb_client.delete_load_balancer(
        LoadBalancerName='loadbalancer-daher')

print('No resources.')
