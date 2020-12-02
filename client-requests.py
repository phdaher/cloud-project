import boto3
import requests

elb_client = boto3.client('elb', region_name='us-west-2')

loadBalancers = elb_client.describe_load_balancers(LoadBalancerNames=['loadbalancer-daher'])['LoadBalancerDescriptions']

if len(loadBalancers) == 1:
    host = loadBalancers[0]['DNSName']
    print("host:", host)

r_post01 = requests.post('http://{0}/tasks/create'.format(host), json={
                     'title': 'teste1', 'pub_date': '2020-12-02T01:48:59Z', 'description': 'testando pela primeira vez'})
print("created task:", r_post01.json())

r_post02 = requests.post('http://{0}/tasks/create'.format(host), json={
                     'title': 'teste2', 'pub_date': '2020-12-02T01:49:59Z', 'description': 'testando pela segunda vez'})
print("created task:", r_post02.json())

r_post03 = requests.post('http://{0}/tasks/create'.format(host), json={
                     'title': 'teste3', 'pub_date': '2020-12-02T01:50:59Z', 'description': 'testando pela terceira vez'})
print("created task:", r_post03.json())

print("getting all tasks...")
r_get = requests.get('http://{0}/tasks'.format(host))
for t in r_get.json():
    print(t)
