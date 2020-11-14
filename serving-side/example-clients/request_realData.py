import json
import requests
import time
from datetime import datetime

url = 'http://140.118.1.26:5000/test_real'
myobj = {'data': 'key1'}

headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json','Date':str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))}
# result  = requests.post(url, data=open('data.json', 'rb'), headers=headers)
# print(result.json())

with open('c8u7KHlpLx4.json') as files:
    data = json.load(files)

for frames in data['data']:
    frames = json.dumps([frames])
    result = requests.post(url, data=frames, headers=headers)
    time.sleep(0.2)
    exit()
