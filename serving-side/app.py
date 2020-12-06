import glob
import os
import time
from gcn import predict
from utils_serving import *
from multiprocessing import Process
from tools.simple_gendata import gendata
from Converter_kinetics import Converter_kinetics
import pymongo
from dbHelper import dbGlobal, dbTemp, dbCounter, dbAction
from pymongo import MongoClient
from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify
import logging
import warnings
import json
from datetime import datetime
import sys
sys.path.append('../gcn_deploy/')


# DEVEL VERSION
warnings.filterwarnings("ignore")


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# client = MongoClient('127.0.0.1', 27017) #Local
client = MongoClient('db', 27017)  # Local
# client = MongoClient(os.environ["DB_PORT_27017_TCP_ADDR"], 27017)

db = client.TryDatabase
global_table = db.global_table
temp_table = db.temp_table
counter_table = db.counter_table
action_table = db.action_table

try:
    global_table.drop()
    temp_table.drop()
    counter_table.drop()
    action_table.drop()
except:
    pass


files = glob.glob('static/unformated/'+'*')
for f in files:
    os.remove(f)
files = glob.glob('static/npy_data/'+'*')
for f in files:
    os.remove(f)
files = glob.glob('static/formated/'+'*')
for f in files:
    os.remove(f)
# print(db)
# print(client.list_database_names())

global_db = dbGlobal(global_table)
temp_db = dbTemp(temp_table)
counter_db = dbCounter(counter_table)
action_db = dbAction(action_table)

max_frame_for_inference = 140  # 50 #140
sliding_frame = 25

maps_action = ['Hand Shaking',	'Hugging',
               'Kicking',	'Pointing',	'Punching', 'Pushing']


@app.route('/test_posenetOriginalGCN', methods=['POST'])
def test_posenetOriginalGCN():
    return True


@app.route('/data', methods=['POST', 'GET'])
def data():
    client_ip = request.remote_addr  # '140.118.1.26'  # request.remote_addr
    prediction_id = action_db.get_action(client_ip=client_ip)
    prediction_name = maps_action[int(prediction_id)]
    status = action_db.get_status(client_ip=client_ip)
    if status != 0:
        return jsonify({
            'Status': status,
            'Prediction': [prediction_id, prediction_name, 'Devel_80'],
            'Confidence Score Other Class (DEVEL)': ['9', '80', '2', '20', '40', '1'],
            'path(forDevel)': action_db.get_path(client_ip=client_ip)
        })
    else:
        return 'Initialize'


@app.route('/test_posenet', methods=['POST'])
def test_posenet():
    if request.method == 'POST':
        client_ip = request.remote_addr
        date_send = str(datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S.%f")[:-3]).replace(' ', '_').replace('/', '-')
        # date_send = str(request.headers['Date']).replace(
        #     ' ', '_').replace('/', '-')

        data = request.json
        data = add_point(data)
        data = reindex(data)
        # TODO: Normalize data
        file_path1 = os.getcwd() + '/static/unformated/' + str(date_send) + '.json'
        with open(file_path1, 'w') as f:
            json.dump(data, f)

        # last_counter   = temp_db.get_last_record(ip_addr=client_ip)
        last_counter = counter_db.last_counter(ip_addr=client_ip)
        data_converted = Converter_kinetics(
            data_path=file_path1, frame_index=last_counter)

        print(last_counter, flush=True)
        # data_path = file_path1, frame_index = last_counter)
        # print('INFO', client_ip, last_counter, flush=True)
        if last_counter > max_frame_for_inference:

            cluster, cluster_list = temp_db.list_cluster(client_ip)
            file_path2 = os.getcwd() + '/static/formated/' + str(date_send) + '.json'
            with open(file_path2, 'w') as f:
                json.dump(cluster, f)

            temp_db.delete_record(ip_addr=client_ip,
                                  time_span=sliding_frame)
            # print('INFO', client_ip, last_counter, flush=True)
            data_path = 'static/formated/'
            data_out_path = 'static/npy_data/' + str(date_send) + '.npy'
            proc = Process(target=predict, args=(
                data_out_path, data_path, action_db, client_ip))
            # print('something2')
            proc.start()
            # print('Inference result (index)', np.argmax(result[0]))
            # print('#############################################')
            action_db.add(client_ip=client_ip,
                          generated_data=data_out_path, prediction='1')
            # action_db.add(client_ip=client_ip,
            #               generated_data=data_out_path, prediction='1')

            # last_counter = dbCounter.get_last_record(ip_addr=client_ip)
            counter_db.reset_counter(
                ip_addr=client_ip, reset_count=last_counter-sliding_frame)
            last_counter = counter_db.last_counter(ip_addr=client_ip)
            temp_db.add(ip_addr=client_ip, transformed_data=data_converted.kinetics_format(
            ), counter=int(last_counter)+1, file_path=file_path1)

            # Store to DB with spesific IP, flag it with "Inferencing"
            return jsonify({
                'Status': '1',
                # 'Prediction': ['1', 'Hand Shaking', '80'],
                # 'Other_Pred': ['9', '80', '2', '20', '40', '1', '15', '50', '20']
            })

        temp_db.add(ip_addr=client_ip, transformed_data=data_converted.kinetics_format(
        ), counter=int(last_counter)+1, file_path=file_path1)
        counter_db.update_counter(ip_addr=client_ip)
        cluster, cluster_list = temp_db.list_cluster(client_ip)

        last_actionDB = action_db.get_action(client_ip=client_ip)
        if (last_actionDB != 0):
            action_db.change_status(
                client_ip=client_ip, new_status='receiving data')
        else:
            pass

        return jsonify({
            'Status': '0',
        })
    return jsonify({
        'detail': 'Failed',
        'return_value': str(1),
    })


@app.route('/show_database', methods=['POST', 'GET'])
def show_database():
    # data = request.json
    # print(data, flush=True)
    data = action_db.list_data()
    # print(data, flush=True)
    # print(list(data), flush=True)
    return jsonify({
        'data': data
    })


@app.route('/posenet', methods=['POST', 'GET'])
def posenet():
    client_ip = request.remote_addr
    date = request.date

    data = request.json

    print(data)
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

    return jsonify({
        'results': 'File Received'
    })


@ app.route("/")
@ cross_origin()
def helloWorld():
    return "Hello, cross-origin-world!"


@app.route('/video_stream', methods=['POST'])
def video_stream():
    return True

# API route
@ app.route('/api', methods=['POST'])
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
    if request.method == 'POST':
        input_data = request.form['data']
        print(input_data)

        print(request.files)
        if 'file' not in request.files:
            return jsonify({
                'detail': 'JSON file not send correctly',
                'return_value': str(0),
            })

        return jsonify({
            'results': 'File Received'
        })


def predict_action():
    pass


if __name__ == '__main__':
    # This is used when running locally.
    app.run(host='0.0.0.0', debug=True)
