"""
This class holds `money` transaction records, including InitMoney, StockValue, LeftMoney, TotalVal.
    TotalVal = StockValue + LeftMoney
Also, since in one day, investors can but stock multiple times, position should also hold records stock's
average holding costs for the convenience of individual stock revenue.
moduleaurther : Wang Wei <wangwei_aperion@163.com>
"""

from Strategy.record import *
import logging

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
        ######### Transaction Logger ##########
        self.logger = logging.getLogger("Main.transaction")
        self.handler = logging.FileHandler("./temp/transaction.csv")
        self.logger.addHandler(self.handler)
        ######### Money Logger ###########
        self.moneylogger = logging.getLogger("Main.money")
        self.moneyhandler = logging.FileHandler("./temp/moneyrecord.csv")
        self.moneylogger.addHandler(self.moneyhandler)
        ######### Position Logger ##########
        self.positionlogger = logging.getLogger("Main.position")
        self.positionhandler = logging.FileHandler("./temp/position.csv")
        self.positionlogger.addHandler(self.positionhandler)

    def totalValadjust(self):
        self.TotalVal = self.LeftMoney + self.StockValue

    def buildstock(self, secID):
        self.Stocks[secID] = PositionRecord(secID, 0, 0, "B")

    def changedate(self, date):
        for key, iterstock in self.Stocks.items():
            iterstock.sellable = iterstock.vol
        self.totalValadjust()
        self.moneylogger.info("{}, {}, {}, {}".format(date, self.LeftMoney, self.StockValue, self.TotalVal))

    def sendrecord(self, onroadorder):
        onroadorder.adjustprice(commision=self.commision, slipage=self.slipage)
        if (onroadorder.dir).upper() == "B":
            self.LeftMoney  -= (onroadorder.price * onroadorder.vol)
        elif (onroadorder.dir).upper() == "S":
            self.Stocks[onroadorder.secID].sellable -= onroadorder.vol

    def cancelrecord(self, onroadorder):
        if (onroadorder.dir).upper() == "B":
            self.LeftMoney += (onroadorder.price * onroadorder.vol)
        elif (onroadorder.dir).upper() == "S":
            self.Stocks[onroadorder.secID].sellable += onroadorder.vol

    def holdrecord(self, transrecord):
        if (transrecord.dir).upper() == "B":
            self.StockValue = self.StockValue + (transrecord.oriprice * transrecord.vol)
            self.totalValadjust()
        elif (transrecord.dir).upper() == "S":
            self.StockValue = self.StockValue - (transrecord.oriprice * transrecord.vol)
            self.totalValadjust()
        else:
            raise Exception
        # Stock Position Adjust
        if transrecord.secID in list(self.Stocks.keys()):
            t_positionrecord = self.Stocks.get(transrecord.secID)
            t_positionrecord.update(transrecord)
            self.positionlogger.info("{}, {}, {}, {}, {}".format(transrecord.date, t_positionrecord.secID, t_positionrecord.avgprice,
                                                             t_positionrecord.vol, t_positionrecord.sellable))
            self.logger.info("{}, {}, {}, {}, {}".format(transrecord.date, transrecord.secID, transrecord.price,
                                                     transrecord.vol, transrecord.dir))
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