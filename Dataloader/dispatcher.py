"""
Dispatcher class contains a number of atomicdispatchers, each opening one connection to database.
moduleaurther : Wang Wei <wangwei_aperion@163.com>
"""

import pymongo
import json
import multiprocessing as mul
from Strategy.strategy import Strategy
from Dataloader.dbadapter import *

class atomicdispatcher(mul.Process):

    # A false implementation: strategy class must be pickable
    # But I haven't studied it.
    def start(self):
        self.initmongo()

    def __init__(self, path = None, strategy = None):
        super(atomicdispatcher, self).__init__()
        if path is None:
            path = "./Storage/stocknames.json"
        self._stocknamefile = open(path, encoding="utf-8")
        self._configstruct = json.load(self._stocknamefile)
        try:
            assert strategy is not None
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

class Dispatcher:

    def __init__(self):
        pass

if __name__ == "__main__":
    strategy1 = Strategy(path = "./Strategy/Config/strategy1.json")
    strategy2 = Strategy(path = "./Strategy/Config/strategy2.json")
    D1 = atomicdispatcher(strategy = strategy1)
    D2 = atomicdispatcher(strategy = strategy2)
    D1.start()
    D2.start()
    for D in mul.active_children():
        print("child   p.name:" + D.name + "\tp.id" + str(D.pid))
