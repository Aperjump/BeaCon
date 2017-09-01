"""
Each atomicdispatcher connects one instance of dbadapter, which encapsulate connection to database,
adapting it to an iterater. Through iterating the database, dbadapter get one namedtuple at a time.
moduleaurther : Wang Wei <wangwei_aperion@163.com>
"""

import pymongo
import json

class dbadapter:

    def __init__(self, mongconct, begin, end, stocks):
        self.connection = mongconct
        self.begin = begin
        self.end = end
        self.stock = stocks
        self.dbiter = None

    def connect(self):
        self.dbiter = self.connection.find({"code":{"$in":self.stock},
                                                 "date":{"$lte":self.end},
                                                 "date":{"$gte":self.begin}}).sort([("date",pymongo.ASCENDING)])
        print("Connect successfully!")
        return self.dbiter

if __name__ == "__main__":
    tempconnect = pymongo.MongoClient()
    tempconnect = tempconnect['StockData']['StockDaily']

    tempiter = dbadapter(tempconnect,"2016-01-01", "2017-05-08", ['600060', '600000'])
    tempiter = tempiter.connect()
    next(tempiter)