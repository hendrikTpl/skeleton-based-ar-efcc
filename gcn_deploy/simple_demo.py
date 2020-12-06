#!/usr/bin/env python
import argparse
import sys
import warnings
warnings.filterwarnings("ignore")
# torchlight
import torchlight
from torchlight import import_class
from tools.simple_gendata import gendata
import time
import numpy as np

def predict():
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
    data_path     = 'kinetics_format/single_test3/'
    data_out_path = 'kinetics_format_test.npy'
    gendata(data_path, data_out_path)
    print('Gen_data_time', time.time()-s2_time)

    # start
    Processor = processors['recognition']
    p = Processor(['--c', 'config/sbu/test.yaml', 
    '--index_data','misal','--id_process', 'misal',
    '--test_feeder_args',"{'data_path': 'kinetics_format_test.npy'}"])

    inference_start = time.time()
    result = p.start()
    print('Inference result (index)', np.argmax(result[0]))
    print('Time for Inference', time.time()-inference_start)
    
# predict()