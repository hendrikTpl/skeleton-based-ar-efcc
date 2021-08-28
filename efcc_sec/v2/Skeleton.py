import json
import numpy as np
from typing import List, Any

class SkeletonECC():
    def __init__(self, 
            skeleton_data, 
            is_encrypted= False, 
            shape=None) -> None:
        self.skeleton_data = skeleton_data
        self.input_type = self.input_type_check()
        self.encrypted = is_encrypted
        self.shape = shape

        self.window_size = 150 # Modify based on training dataset
        self.skeleton_gen = self.skeleton_reader()
        
        if isinstance(skeleton_data, dict):
            raise ValueError("Not support dict values")
        if isinstance(skeleton_data, bytes) and shape == None:
            raise ValueError("Bytes initialization required shape")

    def input_type_check(self):
        if isinstance(self.skeleton_data, list):
            return "origin"
        
        if isinstance(self.skeleton_data, bytes):
            return "bytes"

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if isinstance(self.skeleton_data, list):
            number_of_people = len(self.skeleton_data)
            return {
                "number of detection": number_of_people,
            }
    
    def to_array(self, data) -> List:
        if self.input_type == "origin":
            for N in data:
                X_coordinate = N['pose'][0::2]
                Y_coordinate = N['pose'][1::2]
                Z_coordinate = N['score']
                array = np.array([X_coordinate, Y_coordinate, Z_coordinate])
            return array
        else:
            if not self.encrypted:
                return np.frombuffer(self.skeleton_data).reshape(self.shape)
    
    def to_bytes(self, data) -> List:
        if self.input_type == "origin":
            return self.to_array(data).tobytes()
    
    def skeleton_reader(self):
        for frame in self.skeleton_data:
            index = frame['frame_index']
            skeleton = frame['skeleton']
            yield [index, skeleton]

    def multi_skeleton(self, portion) -> bytes:
        '''
        Use: take a portion of skeleton then flatening then bytes
        Params: 
            portion : the portion of skeleton comapre to # of window size
        Example: 
            window size - 150 frame
            portion - 1/4
        '''
        N = int(portion * self.window_size)
        multi_skeleton_data = b''
        for n in range(N):
            data = self.skeleton_gen.__next__()
            sk_bytes = self.to_bytes(data[1])
            # ind_bytes = bytes(np.array(data[0]).tobytes()) Not sending index for now, --> increase reshaping time in server
            # multi_skeleton_data += ind_bytes
            multi_skeleton_data += sk_bytes
        return multi_skeleton_data


def invert_transform(data):
    a, b = divmod(len(data), 432)
    return np.frombuffer(data).reshape(a, 3, 18)


if __name__ == "__main__":
    with open('./kinec_set1_4_1_0.json') as json_files:
        data = json.load(json_files)

    skeleton_obj = SkeletonECC(skeleton_data=data['data'])
    data = skeleton_obj.multi_skeleton(portion=2)
    
    # for n in range(len(data['data'])):
    #     frame2 = data['data'][n]['skeleton']
    #     ex = SkeletonECC(skeleton_data=frame2, is_encrypted=False, shape=(3,18))
    #     bytes_convert = ex.to_bytes()
    #     print(len(bytes_convert))
    
    # exit()
    # # Client Side
    # ex = SkeletonECC(skeleton_data=frame2, is_encrypted=False, shape=(3,18))
    # bytes_convert = ex.to_bytes()
    
    
    # # Server side
    # ex2 = SkeletonECC(skeleton_data=bytes_convert, is_encrypted=False, shape=(3,18))
    # print((ex2.to_array() == ex.to_array()).all()) #Check data is same
