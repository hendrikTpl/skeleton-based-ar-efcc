#!/usr/bin/env python
import argparse
import sys
sys.path.append('../gcn_deploy/')
import warnings
warnings.filterwarnings("ignore")
# torchlight
import torchlight
from torchlight import import_class
from tools.simple_gendata import gendata
import time
import numpy as np
import os
import glob

def predict(data_out_path, data_path):
    start_time = time.time()
    parser = argparse.ArgumentParser(description='Processor collection')

    processors = dict()
    processors['recognition'] = import_class('processor.recognition.REC_Processor')

    # add sub-parser
    subparsers = parser.add_subparsers(dest='processor')
    for k, p in processors.items():
        subparsers.add_parser(k, parents=[p.get_parser()])

    # read arguments
    arg = parser.parse_args()
  
    s2_time = time.time()
    # data_path     = '../gcn_deploy/kinetics_format/single_test2/'
    # data_path = 'static/formated/'
    # data_out_path = 'static/npy_data/kinetics_format_test.npy'
    gendata(data_path, data_out_path)
    print('Gen_data_time', time.time()-s2_time)
    outpath_config = "{'data_path':" + str(data_out_path) + "}"

    files = glob.glob(data_path+'*')
    for f in files:
        os.remove(f)

    # start
    # Processor = processors['recognition']
    # p = Processor(['--c', 'config/test.yaml', 
    # '--index_data','test_X','--id_process', 'id_y',
    # '--test_feeder_args', "{'data_path': 'static/npy_data/kinetics_format_test.npy'}"])

    # inference_start = time.time()
    # result = p.start()
    # print('Inference result (index)', np.argmax(result[0]))
    # print('Time for Inference', time.time()-inference_start)
    
# predict()