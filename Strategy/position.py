"""
This class holds `money` transaction records, including InitMoney, StockValue, LeftMoney, TotalVal.
    TotalVal = StockValue + LeftMoney
Also, since in one day, investors can but stock multiple times, position should also hold records stock's
average holding costs for the convenience of individual stock revenue.
moduleaurther : Wang Wei <wangwei_aperion@163.com>
"""

from Strategy.record import *

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

    def buildstock(self, secID):
        self.Stocks[secID] = PositionRecord(secID, 0, 0, "B")

    def changedate(self):
        for key, iterstock in self.Stocks.items():
            iterstock.sellable = iterstock.vol

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

    @property
    def leftmoney(self):
        return self.LeftMoney

    @property
    def stockvalue(self):
        return self.stockvalue

    @property
    def totalval(self):
        return self.TotalVal

    @property
    def stock(self):
        return self.Stocks