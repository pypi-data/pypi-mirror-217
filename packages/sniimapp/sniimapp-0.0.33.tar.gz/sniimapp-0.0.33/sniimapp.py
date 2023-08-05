import datetime
from pymongo import MongoClient
import os
import re

class SNIIM():

    def __init__(self, collection, start_date, end_date, product='.*', origin='.*' ):
        self.start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        self.end_date   = datetime.datetime.strptime(end_date,   "%Y-%m-%d")
        self.MONGO_HOST = '18.215.228.120'
        self.MONGO_PORT = 27017    
        self.MONGO_USER = 'sniim_read'  
        self.MONGO_PASSW ='sniim_read_x59m'    
        self.client = MongoClient(self._connection_string)
        self.MONGO_DB = 'sniim'                
        if collection == 'fyh':
            self.db_collection = 'sniim_fyh'
        if collection == 'granos':
            self.db_collection = 'sniim_granos'
        self.db = self.client[self.MONGO_DB]
        self.collection = self.db[self.db_collection]
        self.origin = origin
        self.product = product

    def get_data(self):
        product = rgx = re.compile('.*'+str(self.product)+'.*', re.IGNORECASE)  
        origin  = rgx = re.compile('.*'+str(self.origin)+'.*', re.IGNORECASE)
        return self.collection.find({"fecha":{"$gte":self.start_date,"$lte":self.end_date}, "producto":product, "origen":origin })

    @property
    def _connection_string(self):
        return "mongodb://{0}:{1}@{2}:{3}".format(self.MONGO_USER, self.MONGO_PASSW, self.MONGO_HOST, self.MONGO_PORT)
