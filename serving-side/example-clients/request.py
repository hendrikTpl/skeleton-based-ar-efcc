import requests
import time
from datetime import datetime

url = 'http://140.118.1.26:5000/test_posenet'
myobj = {'data': 'key1'}
for i in range(1):
        
    headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json','Date':str(datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")[:-3])}
    result  = requests.post(url, data=open('data.json', 'rb'), headers=headers)
    print(result.json())
    time.sleep(0.5)