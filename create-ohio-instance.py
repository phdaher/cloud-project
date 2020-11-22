import boto3

ec2 = boto3.resource('ec2', region_name='us-east-2')

# Create a security group and allow SSH inbound rule through the VPC
securitygroup = ec2.create_security_group(
    GroupName='SSH-PG', Description='allow SSH and PGtraffic')
securitygroup.authorize_ingress(
    CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=22, ToPort=22)
securitygroup.authorize_ingress(
    CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=5432, ToPort=5432)


# create a new EC2 instance
instance = ec2.create_instances(
    ImageId='ami-0dd9f0e7df0f0a138',
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',
    KeyName='daher-key',
    SecurityGroupIds=[securitygroup.id],
)[0]

ec2.create_tags(Resources=[instance.id], Tags=[
                {'Key': 'Name', 'Value': 'postgres-daher'}, {'Key': 'Creator', 'Value': 'Daher'}])

print("Created instance", instance.id)
