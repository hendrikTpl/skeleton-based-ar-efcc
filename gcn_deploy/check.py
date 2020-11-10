import numpy as np

data_ori = np.load('kinetics_format/train_data.npy')

data_simpler = np.load('kinetics_format2.npy')

print(data_ori.shape, data_simpler.shape)

print(data_ori[0,0,0,:,0])

print(data_simpler[0,0,0,:,0])