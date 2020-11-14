import numpy as np
import json 

def mid_point(a, b):
    # a and b having format x,y,score
    x = (a[0] + b[0])/2
    y = (a[1] + b[1])/2
    score = (a[2] + b[2])/2
    return x, y, score

def add_point(data):
    '''
    Use to add point number 1, due to there is no middle point between right shoulder and left shoulder.
    Example:
    with open('static/unformated/14-11-2020_15:38:02.json') as files:
        data = json.load(files)
    new_data =add_point(data)
    '''
    json_after = []
    for per_person in data:
        #Point1
        score1 = per_person['keypoints'][5]['score']
        x1 = per_person['keypoints'][5]['position']['x']
        y1 = per_person['keypoints'][5]['position']['y']
        #Point2
        score2 = per_person['keypoints'][6]['score']
        x2 = per_person['keypoints'][6]['position']['x']
        y2 = per_person['keypoints'][5]['position']['y']
        a = (score1, x1, y1)
        b = (score2, x2, y2)

        x, y, score = mid_point(a, b)
        position = {
            'x': x,
            'y': y
        }
        mid = {
            'score': score,
            'part' : 'neck',
            'position':position
        }

        per_person['keypoints'].append(mid)
        # print(per_person['keypoints'])
        json_after.append(per_person)
    # print(json_after[-1])
    return json_after

def reindex(data):
    '''
    Use to reindex from posenet format to openpose format.
    Usage:
    newIndex = reindex(new_data)
    '''

    Wmaps = [0, 15, 14, 17, 16, 5, 2, 6, 3, 7, 4, 11, 8, 12, 9, 13, 10, 1]

    newIndex = []
    for per_person in data:
        keypoint = per_person['keypoints']
        new_keypoint =[]
        for maps in range(18):
            indx = Wmaps.index(maps)
            new_keypoint.append(keypoint[indx])
        per_person['keypoints'] = new_keypoint
        newIndex.append(per_person)
    
    # For check
    # for a,b in enumerate(newIndex[-1]['keypoints']):
    #     print(a, b['part'])
    return newIndex

# #For test
# with open('static/unformated/14-11-2020_15:38:02.json') as files:
#     data = json.load(files)
# new_data = add_point(data)
# newIndex = reindex(new_data)
# print(newIndex)








'''
    maps = {
    'nose':0,
    'leftEye':15,
    'rightEye':14,
    'leftEar':17,
    'rightEar':16,
    'leftShoulder':5,
    'rightShoulder':2,
    'leftElbow':6,   
    'rightElbow':3,
    'leftWrist':7,
    'rightWrist':4,
    'leftHip':11,
    'rightHip':8,
    'leftKnee':12,
    'rightKnee':9,
    'leftAnkle':13,
    'rightAnkle':10,
    'neck':1,
    }
'''