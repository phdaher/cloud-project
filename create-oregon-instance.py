import boto3

ec2 = boto3.resource('ec2', region_name='us-west-2')

user_data = """#!/bin/bash
apt update
git clone https://github.com/phdaher/tasks.git
cd tasks
./install.sh
ufw allow 8080/tcp
shutdown -r now
"""

# create a new EC2 instance
instance = ec2.create_instances(
    ImageId='ami-0ac73f33a1888c64a',
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',
    SecurityGroups=['SSH-DJANGO'],
    UserData=user_data
)[0]

ec2.create_tags(Resources=[instance.id], Tags=[
                {'Key': 'Name', 'Value': 'oregon-daher'}, {'Key': 'Creator', 'Value': 'Daher'}])

print("Created instance", instance.id)