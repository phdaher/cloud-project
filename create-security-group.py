import boto3

ec2 = boto3.resource('ec2', region_name='us-east-2')

# Create a security group and allow SSH inbound rule through the VPC
securitygroup = ec2.create_security_group(
    GroupName='SSH-PG', Description='allow SSH and PG traffic')
securitygroup.authorize_ingress(
    CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=22, ToPort=22)
securitygroup.authorize_ingress(
    CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=5432, ToPort=5432)

print("Created security group", securitygroup.id)