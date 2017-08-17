"""
Each atomicdispatcher connects one instance of dbadapter, which encapsulate connection to database,
adapting it to an iterater. Through iterating the database, dbadapter get one namedtuple at a time.
moduleaurther : Wang Wei <wangwei_aperion@163.com>
"""

import pymongo
import json
class dbadapter(object):

    def __init__(self, mongconct):
        self._connection = mongconct

    def gettime(self, begin, end):
        self._begin = begin
        self._end = end

    def connect(self):
        self._resultiter = self._connection.find({"$and" : [{"time" : {"$gte" : self._begin}},
                                                            {"time" : {"$lte" : self._end }}]})
    # Confused here, should I just implement next() making dbadapater an iterable class,
    # or make it a fully-fledged iterator
    def __iter__(self):
        return self

    def next(self):
        return next(self._resultiter)