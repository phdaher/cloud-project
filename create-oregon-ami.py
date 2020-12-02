import boto3

client = boto3.client('ec2', region_name='us-west-2')

instances = client.describe_instances(Filters=[
    {'Name': 'tag:Name', 'Values': ['oregon-daher']},
    {'Name': 'instance-state-name', 'Values': ['running']}])['Reservations']

if len(instances) == 1:
    instanceId = instances[0]['Instances'][0]['InstanceId']
    image = client.create_image(
        InstanceId=instanceId, Name='ami-daher', NoReboot=True)
    waiter = client.get_waiter('image_available')
    waiter.wait(ImageIds=[image['ImageId']])
    print('Image available.')
