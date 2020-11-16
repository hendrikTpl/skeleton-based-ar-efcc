# DEVEL VERSION
import json
import os
import sys
sys.path.append('../gcn_deploy/')
import warnings
warnings.filterwarnings("ignore")
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
from dbHelper import dbGlobal, dbTemp, dbCounter
import pymongo
from Converter_kinetics import Converter_kinetics

from tools.simple_gendata import gendata
from multiprocessing import Process
from utils_serving import *
from gcn import predict

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# client = MongoClient('127.0.0.1', 27017) #Local
client = MongoClient('db', 27017) #Local
# client = MongoClient(os.environ["DB_PORT_27017_TCP_ADDR"], 27017)

db = client.TryDatabase
global_table = db.global_table
temp_table = db.temp_table
counter_table = db.counter_table

try:
    global_table.drop()
    temp_table.drop()
    counter_table.drop()
except:
    pass

print(db)
print(client.list_database_names())

global_db = dbGlobal(global_table)
temp_db = dbTemp(temp_table)
counter_db = dbCounter(counter_table)

max_frame_for_inference = 15

@app.route('/test_posenet', methods=['POST'])
def test_posenet(): 
    if request.method =='POST':
        client_ip = request.remote_addr
        date_send = str(request.headers['Date']).replace(' ','_').replace('/','-')
        
        data = request.json
        data = add_point(data)
        data = reindex(data)
        file_path1 = os.getcwd() + '/static/unformated/'+ str(date_send) +'.json'
        with open(file_path1, 'w') as f:
            json.dump(data, f)

        # last_counter   = temp_db.get_last_record(ip_addr=client_ip)
        last_counter   = counter_db.last_counter(ip_addr=client_ip)
        data_converted = Converter_kinetics(data_path=file_path1, frame_index=last_counter)

        print('INFO', client_ip, last_counter, flush=True)
        if last_counter>max_frame_for_inference:

            cluster, cluster_list = temp_db.list_cluster(client_ip)
            file_path2 = os.getcwd() + '/static/formated/'+ str(date_send) +'.json'
            with open(file_path2, 'w') as f:
                json.dump(cluster, f)
            
            temp_db.delete_record(ip_addr=client_ip)
            print('INFO', client_ip, last_counter, flush=True)
            #Kinetic GenData from cluster && Predict
            data_path     = 'static/formated/'
            data_out_path = 'static/npy_data/kinetics_format_test.npy'
            # proc = Process(target=predict, args=(data_out_path, data_path))
            # proc.start()
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@', client_ip, last_counter, flush=True)
            # last_counter = dbCounter.get_last_record(ip_addr=client_ip)  
            counter_db.reset_counter(ip_addr= client_ip, reset_count = last_counter-10)
            last_counter = counter_db.last_counter(ip_addr=client_ip) 
            temp_db.add(ip_addr= client_ip, transformed_data=data_converted.kinetics_format(), counter= int(last_counter)+1, file_path=file_path1)
            return jsonify({
                'detail':'Success',
                'return_value': str(0)})

        temp_db.add(ip_addr= client_ip, transformed_data=data_converted.kinetics_format(), counter= int(last_counter)+1, file_path=file_path1)
        counter_db.update_counter(ip_addr= client_ip)
        cluster, cluster_list = temp_db.list_cluster(client_ip)
        return jsonify({
            'detail':'Success',
            'return_value': str(0),
        })
    return jsonify({
            'detail':'Failed',
            'return_value': str(1),
        })

# @app.route

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
