import requests

resp = requests.post('http://34.220.189.219:8080/tasks/create', json={
                     'title': 'teste2', 'pub_date': '2020-12-02T01:48:59Z', 'description': 'testando pela segunda vez'})
print(resp)

r = requests.get('http://34.220.189.219:8080/tasks')
print(r.content)

