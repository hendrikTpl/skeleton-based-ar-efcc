import time
from datetime import datetime
class dbGlobal():
    def __init__(self, database):
        self.database = database

    def add(self, ip_name='0.0.0.0',
            time_stamp = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
            original_data,
            openpose_format_data
            ):
        
        self.database.insert_one({
            'ip_address': ip_name,
            'date_time' : time_stamp,
            'original_data': original_data,
            'openpose_data': openpose_format_data,
        })
        return True
    
class dbAction():
    def __init__(self, database):
        self.database = database

    def add(self, generated_data, list_id):
        self.database.insert_one({
            'generated_data': generated_data,
            'object_id':list_id,
        })
    
class dbTemp():
    def __init__(self, database):
        self.database = database

    def add(self, ip_addr, transformed_data):
        self.database.insert_one({
            'generated_data': ip_addr,
            'object_id':[transformed_data],
        })
    
    def update(self, ip_addr):


