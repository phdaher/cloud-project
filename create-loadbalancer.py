import boto3

client = boto3.client('elb', region_name='us-west-2')

response = client.create_load_balancer(
    AvailabilityZones=['us-west-2a', 'us-west-2b', 'us-west-2c'],
    Listeners=[
        {
            'InstancePort': 8080,
            'InstanceProtocol': 'HTTP',
            'LoadBalancerPort': 80,
            'Protocol': 'HTTP',
        },
    ],
    LoadBalancerName='loadbalancer-daher',
)

print(response['DNSName'])
