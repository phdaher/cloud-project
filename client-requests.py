import requests

host = 'loadbalancer-daher-613198761.us-west-2.elb.amazonaws.com'

resp = requests.post('http://{0}/tasks/create'.format(host), json={
                     'title': 'teste2', 'pub_date': '2020-12-02T01:48:59Z', 'description': 'testando pela segunda vez'})
print(resp)

r = requests.get('http://{0}/tasks'.format(host))
print(r.content)

