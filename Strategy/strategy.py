"""
This class holds `money` transaction records, including InitMoney, StockValue, LeftMoney, TotalVal.
    TotalVal = StockValue + LeftMoney
Also, since in one day, investors can but stock multiple times, position should also hold records stock's
average holding costs for the convenience of individual stock revenue.
moduleaurther : Wang Wei <wangwei_aperion@163.com>
"""

import json
from Strategy.record import *
from Strategy.position import *

class Strategy(object):

    def __init__(self, path):
        if path is None:
            raise Exception
        else:
            self.count = 0
            self._pathfile = open(path, encoding="utf-8")
            self._strategystruct = json.load(self._pathfile)
            self._stock = self._strategystruct['stocklist']
            self._begin = self._strategystruct['starttime']
            self._end = self._strategystruct['endtime']
            # record orders which have not closed deal

    def setaccount(self, position = None):
        if position is None:
            self._position = Position(1000000, commision = 0.001, slipage = 0.001)
            self.onroad = OnRoadOrderManager(position = self._position)

    def OnEvent(self, item):
        raise Exception

    def sendorder(self, onroadorder):
        self.onroad.get(onroadorder)


if __name__ == "__main__":
    strategy1 = Strategy("./Strategy/Config/strategy1.json")