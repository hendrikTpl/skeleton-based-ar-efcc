import requests
import time
from datetime import datetime
import json
url = 'http://140.118.1.26:5000/show_database'
headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json','Date':str(datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")[:-3])}
result  = requests.post(url, json=json.dumps({'coba':'coba'}))
print(result.json())