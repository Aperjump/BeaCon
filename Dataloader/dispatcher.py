"""
Dispatcher class contains a number of atomicdispatchers, each opening one connection to database.
moduleaurther : Wang Wei <wangwei_aperion@163.com>
"""

import pymongo
import json
from Dataloader.dbadapter import *

DBmap = {"D" : "StockDaily", "1min" : "Onemin", "5min" : "Fivemin", "15min" : "Fifteenmin", "30min" : "Thirtymin"}

class Dispatcher(object):

    def __init__(self, path = None):
        if path is None:
            path = "./backtestingconfig.json"
        self.config = json.load(open(path))
        self.begin = self.config['begin']
        self.end = self.config['end']
        self.freq = self.config['freq']
        self.initmongo()
        self.map = {}
        # stocks = map.key()
        self.stocks = None

    def initmongo(self):
        self.client = pymongo.MongoClient(self.config['Mongo']['mongodburl'])
        try:
            self.db = self.client[self.config['Mongo']['mongodocument']]
        except Exception as e:
            print("Cannot find the correct database, try it again.")
        # Use freq find data base document
        self.stockdb = self.db[DBmap[self.freq]]

    def register(self, secid, strategy):
        self.map[secid] = strategy

    # After register phase finish, begin search in the database
    def loaddata(self):
        if self.stocks is None:
            self.stocks = self.map.keys()
        self.dbconnect = dbadapter(self.stockdb, self.begin, self.end, self.stocks)

    def run(self):
        for it in self.dbconnect:
            tempstrategylist = self.map[it['code']]
            for tempstrategy in tempstrategylist:
                tempstrategy.onbar(it)


if __name__ == "__main__":
    tempconnect = Dispatcher("E:/QuantFrameWork/BeaCon/Dataloader/backtestconfig.json")
    tempconnect.stocks = ['600060','600000']
    tempconnect.loaddata()