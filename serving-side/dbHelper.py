import time
from datetime import datetime
import pymongo
import os
class dbGlobal():
    '''    
    database = name of the database
    original_data = path to the original json from internet request
    openpose_data = path to the json after convert to kinetics format
    '''
    def __init__(self, database):
        self.database = database

    def add(self, ip_name,
            original_data,
            openpose_format_data
            ):
        try:
            self.database.insert_one({
                'ip_address': ip_name,
                'date_time' : str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
                'original_data': original_data,
                'openpose_data': openpose_format_data,
                })
            return "Successfully added to database"
        except Exception as e:
            return 'Data fails to save in DB with error = '+ str(e)

    
class dbAction():
    def __init__(self, database):
        self.database = database

    def add(self, generated_data, client_ip, prediction):
        self.database.insert_one({
            'generated_data': generated_data,
            'client_ip': client_ip, 
            'prediction': prediction
        })
    
    def list_data(self):
        cursor = self.database.find()
        list_data = []
        for data in cursor:
            dt = {
                'Source_IP' : data['client_ip'],
                'Data_path' : data['generated_data'],
                'Prediction_Result': data['prediction'],
            }
            # print(dt)
            list_data.append(dt)
        return list_data
    
class dbTemp():
    def __init__(self, database):
        self.database = database

    def add(self, ip_addr, transformed_data, counter, file_path):
        self.database.insert_one({
            'ip_address': ip_addr,
            'data':transformed_data,
            'counter' : counter, 
            'file_name':file_path, 
        })

    def get_last_record(self, ip_addr):
        report = self.database.find_one(
            {'ip_address': ip_addr},
            sort=[( '_id', pymongo.DESCENDING )]
            )
        try:
            return report['counter']
        except:
            return 0

    def delete_record(self, ip_addr, time_span=10):
        report = self.database.find(
            {'ip_address': ip_addr}).sort("_id", 1)
        i = 0
        for data in report:
            if i >= time_span:
                break
            print(data['file_name'], data['counter'])
            try:
                self.database.remove({"file_name": data['file_name']})
                os.remove(data['file_name'])
            except Exception as e:
                print(e)
                pass
            i = i+1
        print('REMAIN')
        report = self.database.find(
            {'ip_address': ip_addr}).sort("counter", 1)
        for data in report:
            print(data['file_name'], data['counter'])

    def list_cluster(self, ip_addr):
        report = self.database.find(
            {'ip_address': ip_addr}
            )
        try: 
            json_form = []
            file_lit = []
            for x in report:
                json_form.append(x['data'])
                file_lit.append(x['file_name'])
            json_form = {
                'data': json_form,
                'label': 'Unknown',
                'label_index': int(0)
            }
            return json_form , file_lit
        except:
            return 0

    def get_cluster(self, ip_addr):
        report = self.database.find(
            {'ip_address': ip_addr}
            )
        try: 
            json_form = []
            for x in report:
                json_form.append(x)
            return json_form
        except:
            return 0

    
    # def update(self, ip_addr):

class dbCounter():
    def __init__(self, database):
        self.database = database

    def add(self, ip_addr, counter):
        self.database.insert_one({
            'ip_address': ip_addr,
            'last_counter' : counter, 
        })

    def last_counter(self, ip_addr):
        report = self.database.find_one(
                {'ip_address': ip_addr}
        )
        try:
            return report['last_counter']
        except:
            return 0
    
    def update_counter(self, ip_addr):
        last_counter = self.last_counter(ip_addr)
        self.database.update_one(
            {'ip_address': ip_addr},
            {"$set": 
                {"last_counter": last_counter+1}},
            upsert=True
        )

    def reset_counter(self, ip_addr, reset_count):
        last_counter = self.last_counter(ip_addr)
        self.database.update_one(
            {'ip_address': ip_addr},
            {"$set": 
                {"last_counter": reset_count}}
        )
        

