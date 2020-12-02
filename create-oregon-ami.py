import boto3

client = boto3.client('ec2', region_name='us-west-2')

# Cria o AMI baseado na instancia que está rodando em oregon
reservations = client.describe_instances(Filters=[
    {'Name': 'tag:Name', 'Values': ['oregon-daher']},
    {'Name': 'instance-state-name', 'Values': ['running']}])['Reservations']

# 
if len(reservations) == 1:
    instanceId = reservations[0]['Instances'][0]['InstanceId']
    image = client.create_image(
        InstanceId=instanceId, Name='ami-daher', NoReboot=True)
    waiter = client.get_waiter('image_available')
    waiter.wait(ImageIds=[image['ImageId']])
    print('Image available.')
    client.terminate_instances(InstanceIds=[instanceId])