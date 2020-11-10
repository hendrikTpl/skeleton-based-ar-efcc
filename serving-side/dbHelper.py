import time
from datetime import datetime
import pymongo
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

    def add(self, generated_data, list_id):
        self.database.insert_one({
            'generated_data': generated_data,
            'list_object_id':list_id,
        })
    
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

    def delete_record(self, ip_addr):
        try:
            self.database.remove({"ip_address": ip_addr})
            return True
        except:
            return False

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


