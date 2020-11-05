import json

class Converter():
    def __init__(self, data_path):
        self.path = data_path
        self.data = self.reader()
        self.key  = ['score', 'keypoints']

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
    

data = Converter('data.json')
print(data.n_detection)
print(data.get_detection(1))    