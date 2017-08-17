"""
Construct 6 data bases, each represent one data type:
stock daily K bar, 5 min K bar, 15 min K bar, 30 min K bar, 60 min K bar
and a stock daily K bar aggregation(contain all stock data)
moduleaurther : Wang Wei <wangwei_aperion@163.com>
"""

import tushare as ts
import pandas as pd
import pymongo
import json
import time

class StorageConfig(object):
    """
    record info for permanent storage
    """
    def __init__(self, path = None):
        if path is None:
            path = "./stocknames.json"
        self._stocknamefile = open(path, encoding="utf-8")
        self.loadstocknames()

    def loadstocknames(self):
        self._configstruct = json.load(self._stocknamefile)
        self._stocknames = self._configstruct['stocklist']
        print("used stocks: ", self._stocknames)
    def initmongo(self):
        # Connect to Mongodb
        self._client = pymongo.MongoClient(self._configstruct['mongodburl'])
        self._db = self._client[self._configstruct['mongocollection']]
    def insert(self):
        for iter in self._stocknames:
            try:
                temprecord = ts.get_hist_data(iter, ktype = self._configstruct["timeinterval"],
                                              start = self._configstruct['starttime'])
                tempcollection = self._db[iter]
                temprecord['time'] = temprecord.index
                tempcollection.insert_many(json.loads(temprecord.to_json(orient='records')))
                print(iter + " insert finish!")
            except Exception as e:
                # write in log files
                print(e)


class UpdateConfig(StorageConfig):
    """
    Same config as StorageConig, but will download current day data
    """
    def __init__(self, path=None):
        StorageConfig.__init__(self, path)
        self._today =time.strftime('%Y-%m-%d',time.localtime(time.time()))
    def loadstocknames(self):
        self._configstruct = json.load(self._stocknamefile)
        self._stocknames = self._configstruct['stocklist']
        # change update time ticker
        self._configstruct['starttime'] = self._today
        print("used stocks: ", self._stocknames)

