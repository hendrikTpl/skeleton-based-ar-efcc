import os
import sys
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
from dbHelper import dbGlobal, dbTemp
import pymongo
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

client = MongoClient('127.0.0.1', 27017)
db = client.TryDatabase
global_table = db.global_table
temp_table = db.temp_table

try:
    global_table.drop()
    temp_table.drop()
except:
    pass

print(db)
print(client.list_database_names())

global_db = dbGlobal(global_table)
temp_db = dbTemp(temp_table)

max_frame_for_inference = 5

@app.route('/test_db',  methods=['POST', 'GET'])
def test_db():
    ip_address = '0.0.0.0'
    last_counter = temp_db.get_last_record(ip_addr=ip_address)
    print(last_counter)
    print('Got it')
    cursor = temp_table.find_one(sort=[( '_id', pymongo.DESCENDING )])
    print(cursor)
    if last_counter>max_frame_for_inference:
        temp_db.delete_record(ip_addr=ip_address)
        last_counter = temp_db.get_last_record(ip_addr=ip_address)
        temp_db.add(ip_addr= ip_address, transformed_data='path', counter= int(last_counter)+1)
        return 'Test DB'
 
    temp_db.add(ip_addr= ip_address, transformed_data='path', counter= int(last_counter)+1)
    
    return 'Test DB'

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


@app.route("/")
@cross_origin()
def helloWorld():
  return "Hello, cross-origin-world!"


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

def predict_action():
    pass

if __name__ == '__main__':
    # This is used when running locally.
    app.run(host='0.0.0.0', debug=True)
