import requests
from flask import Flask, request
import numpy as np

app = Flask(__name__)

@app.route('/test', methods=['POST'])
def test():
    data = request.data
    slicer = '###'
    slicer = slicer.encode('utf-8')
    data = data.split(slicer)
    print('Config', data[0].decode('utf-8'))
    image =  np.fromstring(data[1])
    image = image.reshape(640,480)
    print('Data', image.shape)
    return "Success"

if __name__ == '__main__':
    # This is used when running locally.
    app.run(host='0.0.0.0', port=5000, debug=True)