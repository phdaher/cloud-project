import boto3

ec2 = boto3.resource('ec2', region_name='us-west-2')

# Get ohio instance public ip
ohio_client = boto3.client('ec2', region_name='us-east-2')
instances = ohio_client.describe_instances(Filters=[
    {'Name': 'tag:Name', 'Values': ['postgres-daher']},
    {'Name': 'instance-state-name', 'Values': ['running']}])['Reservations']
if len(instances) == 1:
    ohio_publicIP = instances[0]['Instances'][0]['PublicIpAddress']
print(ohio_publicIP)

user_data = """#!/bin/bash
apt update
git clone https://github.com/phdaher/tasks.git
cd /tasks/portfolio
sed -i "s/node1/{0}/g" settings.py
cd /tasks
./install.sh
ufw allow 8080/tcp
shutdown -r now
""".format(ohio_publicIP)

# create a new EC2 instance
instance = ec2.create_instances(
    ImageId='ami-0ac73f33a1888c64a',
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',
    KeyName='daher-key',
    SecurityGroups=['SSH-DJANGO'],
    UserData=user_data
)[0]

ec2.create_tags(Resources=[instance.id], Tags=[
                {'Key': 'Name', 'Value': 'oregon-daher'}, {'Key': 'Creator', 'Value': 'Daher'}])

# Espera estar com o status o para ir para a próxima etapa (AMI)
ec2_client = boto3.client('ec2', region_name='us-west-2')
waiter = ec2_client.get_waiter('instance_status_ok')
waiter.wait(InstanceIds=[instance.id])

print("Created instance", instance.id)
