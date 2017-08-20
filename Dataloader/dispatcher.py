"""
Dispatcher class contains a number of atomicdispatchers, each opening one connection to database.
moduleaurther : Wang Wei <wangwei_aperion@163.com>
"""

import pymongo
import json
import multiprocessing as mul
from Strategy.strategy import strategy
from dbadapter import *
class atomicdispatcher(mul.Process):

    def start(self, path = None, strategy = None):
        self.__init__(path, strategy)
        self.initmongo()

    def __init__(self, path = None, strategy = None):
        if path is None:
            path = "../Strategy/Config/strategy1.json"
        self._stocknamefile = open(path, encoding="utf-8")
        self._configstruct = json.load(self._stocknamefile)
        try:
            assert strategy != None
        except AssertionError as e:
            print("Missing strategy, try to find one! ")
        self._strategy = strategy

    def initmongo(self):
        self._client = pymongo.MongoClient(self._configstruct['mongodburl'])
        try:
            self._db = self._client[self._configstruct['mongocollection']]
            self._stockdb = self._db[self._strategy._stock]
        except pymongo.CollectionInvalid as e:
            print("Cannot find the correct database, try it again.")
        # init ierators
        self._dbconnect = dbadapter(self._stockdb, self._strategy._begin, self._strategy._end)

    def run(self):
        for item in self._dbconnect:
            self._strategy.OnEvent(item)

