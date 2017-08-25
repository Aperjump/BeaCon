"""
This class holds `money` transaction records, including InitMoney, StockValue, LeftMoney, TotalVal.
    TotalVal = StockValue + LeftMoney
Also, since in one day, investors can but stock multiple times, position should also hold records stock's
average holding costs for the convenience of individual stock revenue.
moduleaurther : Wang Wei <wangwei_aperion@163.com>
"""

import json

class TransactionRecord(object):

    def __init__(self, secID, price, vol, direc):
        self.secID = secID
        self.price = price
        self.vol = vol
        # dir = 'B' means "Buy"
        # dir = 'S' means "Sell"
        self.dir = direc

    def topositionrecord(self):
        return PositionRecord(self.secID, self.price, self.vol, self.direc)

    def adjustprice(self, commision = None, slipage = None):
        if (self.dir).upper() == "B":
            self.price = self.price * (1 + slipage) * (1 + commision)
        elif (self.dir).upper() == "S":
            self.price = self.price * (1 - slipage) * (1 - commision)
        else:
            raise Exception

class PositionRecord(object):

    def __init__(self, secID, price, vol, direc):
        self.secID = secID
        self.avgprice = price
        self.vol = vol
        self.dir = direc

    def update(self, transrecord):
        if (transrecord.dir).upper() == "B":
            temptotalvol = self.vol + transrecord.vol
            self.avgprice = (self.avgprice * self.vol + transrecord.price * transrecord.vol) / temptotalvol
            self.vol = temptotalvol
        elif (transrecord.dir).upper() == "S":
            temptotalvol = self.vol - transrecord.vol
            try:
                assert temptotalvol > 0
            except AssertionError as e:
                print("Prohibit short stocks")
            # for log purpose
            earned = (self.avgprice - transrecord.price) * transrecord.vol
            self.avgprice = (self.avgprice * self.vol - transrecord.price  * transrecord.vol)  / temptotalvol
        else:
            raise Exception

class Position(object):

    def __init__(self, initamount, commision = 0, slipage = 0):
        # Set initial account
        self.InitMoney = initamount
        self.LeftMoney = initamount
        self.StockValue = 0
        self.TotalVal = initamount
        self.Stocks = {}
        self.commision = commision
        self.slipage = slipage

    def totalValadjust(self):
        self.TotalVal = self.LeftMoney + self.StockValue

    def holdrecord(self, transrecord):
        transrecord.adjustprice(commision = self.commision, slipage = self.slipage)
        ## Account Value Change
        if (transrecord.dir).upper() == "B":
            self.LeftMoney = self.LeftMoney - (transrecord.price * transrecord.vol)
            self.StockValue = self.StockValue + (transrecord.price * transrecord.vol)
            self.totalValadjust()
        elif (transrecord.dir).upper() == "S":
            self.LeftMoney = self.LeftMoney + (transrecord.price * transrecord.vol)
            self.StockValue = self.StockValue - (transrecord.price * transrecord.vol)
            self.totalValadjust()
        else:
            raise Exception
        # Stock Position Adjust
        if transrecord.secID in self.Stocks.keys():
            t_positionrecord = self.Stocks.get(transrecord.secID)
            t_positionrecord.update(transrecord)
        else:
            self.Stocks.__setitem__({transrecord.secID : transrecord.topositionrecord()})

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