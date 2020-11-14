import json

class Converter_kinetics():
    '''
        Use to convert data from posenet request to kinetics data.
        Example use:
        data = Converter_kinetics(data_path='data.json', frame_index=1)
        print(data.kinetics_format())
    '''
    def __init__(self, data_path, frame_index):
        self.path = data_path
        self.data = self.reader()
        self.key  = ['score', 'keypoints']
        self.frame_index = frame_index

    def reader(self):
        with open(self.path, 'r') as file:
            data = json.load(file)
        self.n_detection = len(data)
        return data

    def get_score(self, person_id):
        if person_id > self.n_detection:
            return 'Error, the max detection is '+ str(self.n_detection)
        return self.data[person_id]['score']

    def get_detection(self, person_id):
        if person_id > self.n_detection:
            return 'Error, the max detection is '+ str(self.n_detection)
        return self.data[person_id]['keypoints']

    def kinetics_format(self, n_max = 2):
        perFrame = []
        for person_id in range(n_max):
            detection = []
            scores = []
            for x in self.get_detection(person_id):
                x_coor = x['position']['x']
                y_coor = x['position']['y']
                score  = x['score']
                detection.append(x_coor)
                detection.append(y_coor)
                scores.append(score)
            perId = {
                'pose': detection,
                'score':scores
            }
            perFrame.append(perId)
        # print(perFrame)
        perFrame = {
            'frame_index':self.frame_index,
            'skeleton':perFrame,
        }
        return perFrame

# data = Converter_kinetics(data_path='data.json', frame_index=1)
# print(data.kinetics_format())
