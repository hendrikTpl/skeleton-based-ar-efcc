#!/usr/bin/env python
import sys
sys.path.append('../gcn_deploy')
import glob
import os
import numpy as np
import time
from tools.simple_gendata import gendata
from torchlight import import_class
import torchlight
import argparse
import warnings
import sys
#sys.path.append('../gcn_deploy/')
warnings.filterwarnings("ignore")
# torchlight


def predict(data_out_path, data_path, action_db, client_ip):
    start_time = time.time()
    parser = argparse.ArgumentParser(description='Processor collection')

    processors = dict()
    processors['recognition'] = import_class(
        'processor.recognition.REC_Processor')

    # add sub-parser
    subparsers = parser.add_subparsers(dest='processor')
    for k, p in processors.items():
        subparsers.add_parser(k, parents=[p.get_parser()])

    # read arguments
    arg = parser.parse_args()

    s2_time = time.time()
    gendata(data_path, data_out_path, max_frame = 160)
    print('Gen_data_time', time.time()-s2_time)
    outpath_config = "{'data_path':" +"'"+ str(data_out_path)+"'"+ "}"

    files = glob.glob(data_path+'*')
    for f in files:
        os.remove(f)

    # start
    Processor = processors['recognition']
    p = Processor(['--c', 'config/test.yaml',
                    '--index_data', 'test_X', '--id_process', 'id_y',
                    '--test_feeder_args', outpath_config])

    inference_start = time.time()
    result = p.start()
    print('Time for Inference', time.time()-inference_start)
    # After got result, update last db of the spesific IP, with the gcn output, Andflag the data by "Done Predict"
    action_db.add(client_ip=client_ip,generated_data=data_out_path, prediction=str(np.argmax(result[0])))
    action_db.change_status(client_ip=client_ip, new_status='Done Inferencing')
    return result

