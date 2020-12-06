import os
import sys
import pickle
import argparse

import numpy as np
from numpy.lib.format import open_memmap


sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from feeder.simple_feeder import Feeder_kinetics

def gendata(
        data_path,
        data_out_path,
        num_person_in=2,  #observe the first 5 persons
        num_person_out=2,  #then choose 2 persons with the highest score
        max_frame=300):

    feeder = Feeder_kinetics(
        data_path=data_path,
        num_person_in=num_person_in,
        num_person_out=num_person_out,
        window_size=max_frame,
        frame_max=max_frame)

    sample_name = feeder.sample_name
    sample_label = []

    fp = open_memmap(
        data_out_path,
        dtype='float32',
        mode='w+',
        shape=(len(sample_name), 3, max_frame, 18, num_person_out))

    for i, s in enumerate(sample_name):
        data = feeder[i]
        fp[i, :, 0:data.shape[1], :, :] = data




