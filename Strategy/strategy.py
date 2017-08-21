"""
Construct a strategy template, can be used to build more sophistcated strategy class
moduleaurther : Wang Wei <wangwei_aperion@163.com>
"""

import json
from Strategy.position import *
from abc import ABCMeta


class OnRoadOrder(object):

    def __init__(self):
        self.secID = "000000"
        self.price = 10
        self.vol = 100
        self.dir = "B"
        self.count = 0
        self.alive = False

    def build(self, secID, price, vol, direc):
        self.secID = secID
        self.price = price
        self.vol = vol
        # dir = 'B' means "Buy"
        # dir = 'S' means "Sell"
        self.dir = direc
        self.count = 0
        self.alive = True

    def destruct(self):
        self.secID = "000000"
        self.price = 10
        self.vol = 100
        self.dir = "B"
        self.count = 0
        self.alive = False

    def totransactionrecord(self):
        return TransactionRecord(self.secID, self.price, self.vol, self.dir)

class OnRoadOrderManager(object):

    def __init__(self, position, maxnum = 5, time2cancel = 10):
        self.position = position
        self.time2cancel = time2cancel
        self.recordlist = list()
        for i in range(maxnum):
            self.recordlist.append(OnRoadOrder())

    def get(self,OnRoadOrder):
        positionflag = False
        for item in self.recordlist:
            if (item.alive):
                item.build(OnRoadOrder.secID,
                           OnRoadOrder.price,
                           OnRoadOrder.vol,
                           OnRoadOrder.dir)
                positionflag = True
                break
            else:
                pass
        if positionflag:
            print("Insert Success.")
        else:
            print("No available position.")

    def checktrade(self, stockdata):
        for record in self.recordlist:
            if stockdata.low <= record.price and stockdata.high >= record.price:
                self.position.holdrecord(record.totransactionrecord)
                record.distruct()
            else:
                if record.count >= self.time2cancel:
                    record.distruct()
                else:
                    record.count += 1


class Strategy(ABCMeta):

    def __init__(cls, path):
        if path is None:
            raise Exception
        else:
            cls._pathfile = open(path, encoding="utf-8")
            cls._strategystruct = json.load(cls._pathfile)
            cls._stock = cls._strategystruct['stocklist']
            cls._begin = cls._strategystruct['starttime']
            cls._end = cls._strategystruct['endtime']
            # record orders which have not closed deal
            cls.onroad = OnRoadOrderManager()

    def setaccount(cls, position = None):
        if position is None:
            cls._position = Position(1000000, commision =.001, slipage = .001)
            cls.onroad = OnRoadOrderManager(position = cls._position)

    def OnEvent(cls, item):
        raise Exception

    def sendorder(cls, onroadorder):
        cls.onroad.get(onroadorder)


if __name__ == "__main__":
    strategy1 = Strategy("./Strategy/Config/strategy1.json")