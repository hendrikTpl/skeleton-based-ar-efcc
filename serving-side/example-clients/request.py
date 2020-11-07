import requests
import time


url = 'http://140.118.1.26:5000/communicate'
myobj = {'data': 'key1'}

file_json =  {'file': open('data/s01s02-01-001.json', 'rb')}

for i in range (10):
    t1 = time.time()
    result = requests.post(url, data=myobj, files=file_json)
    print('Network Latency  ', time.time()-t1)
    print('Message received ',result.json()['results'])

