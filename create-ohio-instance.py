import boto3

ec2 = boto3.resource('ec2', region_name='us-east-2')

db_user = 'cloud'
db_name = 'tasks'

user_data = """#!/bin/bash
apt update
apt install postgresql postgresql-contrib -y
sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/g" /etc/postgresql/10/main/postgresql.conf
sed -i "s/peer/trust/g" /etc/postgresql/10/main/pg_hba.conf
sed -i "$ a host all all all trust" /etc/postgresql/10/main/pg_hba.conf
ufw allow 5432/tcp
systemctl restart postgresql
createuser -U postgres -s {0}
createdb -U postgres -O {0} {1}
""".format(db_user, db_name)

# create a new EC2 instance
instance = ec2.create_instances(
    ImageId='ami-0dd9f0e7df0f0a138',
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',
    KeyName='daher-key',
    SecurityGroups=['SSH-PG'],
    UserData=user_data
)[0]

ec2.create_tags(Resources=[instance.id], Tags=[
                {'Key': 'Name', 'Value': 'postgres-daher'}, {'Key': 'Creator', 'Value': 'Daher'}])

print("Created instance", instance.id)
