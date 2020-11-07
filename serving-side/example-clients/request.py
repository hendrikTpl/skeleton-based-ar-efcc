import requests
import time
from datetime import datetime

url = 'http://140.118.1.26:5000/test_posenet'
myobj = {'data': 'key1'}



headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json',
'Date':str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))}
result  = requests.post(url, data=open('data.json', 'rb'), headers=headers)
print(result.json())
exit()
file_json =  {'file': open('data.json', 'rb')}

print(file_json)

exit()
for i in range (5):
    t1 = time.time()
    result = requests.post(url, data=myobj, files=file_json)
    print(result.json())
    print('Network Latency  ', time.time()-t1)
    print('Message received ', result.json())

