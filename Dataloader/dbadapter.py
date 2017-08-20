"""
Each atomicdispatcher connects one instance of dbadapter, which encapsulate connection to database,
adapting it to an iterater. Through iterating the database, dbadapter get one namedtuple at a time.
moduleaurther : Wang Wei <wangwei_aperion@163.com>
"""

import pymongo
import json

class dbadapter:

    def __init__(self, mongconct, begin, end):
        self._connection = mongconct
        self._begin = begin
        self._end = end
        self.connect()
    def connect(self):
        self._resultiter = self._connection.find({"$and" : [{"time" : {"$gte" : self._begin}},
                            {"time" : {"$lte" : self._end }}]}).sort([("time",pymongo.ASCENDING)])
    # Confused here, should I just implement next() making dbadapater an iterable class,
    # or make it a fully-fledged iterator
    def __iter__(self):
        return dbiter(self)

class dbiter:

    def __init__(self, dbadapter):
        self._db = dbadapter._resultiter

    def __iter__(self):
        return self

    def __next__(self):
        try:
            temp = next(self._db)
            return temp
        except:
             raise StopIteration()

if __name__ == "__main__":
    tempconnect = pymongo.MongoClient()
    tempconnect = tempconnect['EquityData']['600060']
    tempiter = dbadapter(tempconnect,"2016-01-01", "2017-05-08")
    for i in tempiter:
        print(i)