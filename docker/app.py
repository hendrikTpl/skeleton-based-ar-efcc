import os
import sys
import logging
from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

client = MongoClient(os.environ["DB_PORT_27017_TCP_ADDR"], 27017)
db = client.appdb

@app.route("/")
@cross_origin()
def helloWorld():
    print('Got it')
    return "Hello, cross-origin-world!!!!!!!!!!!!!!!"


# API route
@app.route('/api', methods=['POST'])
def api():
    """API function

    All model-specific logic to be defined in the get_model_api()
    function
    """
    input_data = request.form['data']
    # app.logger.info("api_input: " + str(input_data))
    # output_data = model_api(input_data)
    # app.logger.info("api_output: " + str(output_data))
    print(input_data)
    response = jsonify({
        'Response': 'OK'
    })
    return response

@app.route('/communicate', methods=['POST', 'GET'])
def communicate():
    if request.method =='POST':
        input_data = request.form['data']
        print(input_data)

        print(request.files)
        if 'file' not in request.files:
            return jsonify({
                'detail':'JSON file not send correctly',
                'return_value': str(0),
            })
            
        return jsonify({
            'results':'File Received'
        })

import json
@app.route('/posenet', methods=['POST', 'GET'])
def posenet():
    client_ip = request.remote_addr
    date = request.date
    
    data = request.json
    
    print(data)
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)
            
    return jsonify({
        'results':'File Received'
    })

def predict_action():
    pass

@app.route('/test_db',  methods=['POST', 'GET'])
def test_db():
    print('Got it')
    return 'Test DB'

if __name__ == '__main__':
    # This is used when running locally.
    app.run(host='0.0.0.0', debug=True)
