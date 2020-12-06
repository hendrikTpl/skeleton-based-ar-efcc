import requests
import numpy as np

url = 'http://0.0.0.0:5091/test'

arr = np.random.rand(640, 480)
print(arr.shape)
arr = arr.tobytes()
slicer = '###'
slicer = slicer.encode('utf-8')
storing = 'storing=True'
storing = storing.encode('utf-8')

sent_req = storing+slicer+arr
response = requests.post(url, sent_req)