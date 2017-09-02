"""

moduleaurther : Wang Wei <wangwei_aperion@163.com>
"""

import json
from Strategy.record import *
from Strategy.position import *
from Dataloader.dispatcher import *
import pandas as pd
import logging

class StrategyTemplate(object):

    def __init__(self, path):
        if path is None:
            raise Exception
        else:
            self.sellablemap = {}
            self.config = json.load(open(path))
            self.stock = self.config['stocklist']
            # record orders which have not closed deal
            self.date = None
            self.reforder = 0
            self.onroad = {}
        self.logger = logging.getLogger("Main.strategy")
        self.mainlogger = logging.getLogger("Main")
        self.logger.addHandler(logging.FileHandler("./temp/Sendorder.csv"))

    def setdispatcher(self, dispatcher):
        self.dispatcher = dispatcher
        self.reg2dispatcher()

    def reg2dispatcher(self):
        for iterstock in self.stock:
            self.dispatcher.register(iterstock, self)

    def setaccount(self, position = None):
        if position is None:
            self.position = Position(self.config['initmoney'], commision = self.config['commision'],
                                     slipage = self.config['slipage'])
        # DEPRECATED
        # self.onroad = OnRoadOrderManager(position = self.position)

    def start(self):
        self.setaccount()
        for itestock in self.stock:
            self.position.buildstock(itestock)

    def onbar(self, item):
        if item["volume"] == 0:
            pass
        else:
            ######## Time    Control     ##########
            if self.date is None:
                self.start()
                self.mainlogger.info("Begin backtesting : " + item["date"])
                self.date = pd.to_datetime(item["date"]).date()
            if pd.to_datetime(item["date"]).date() > self.date:
                self.date = pd.to_datetime(item["date"]).date()
                self.position.changedate(self.date)
                self.mainlogger.info("Backtesting on : " + item["date"])
            ######## Clear Untrade Order ##########
            self.clearorder(item)
            ######## User Code: Signal   ##########
            self.strategysignal(item)

    def strategysignal(self, item):
        pass

    def clearorder(self, item):
        for key,order in self.onroad.items():
            if order.secID == item['code']:
                if order.price <= item["high"] and order.price >= item["low"]:
                    self.mainlogger.info("Successful Transaction : secID : {}, price : {}, vol : {}, "
                          "dir : {}".format(order.secID, round(order.price, 2), order.vol, order.dir))
                    self.position.Stocks[order.secID].update(order.totransactionrecord(self.date))
                    self.position.holdrecord(order.totransactionrecord(self.date))
            else:
                pass

    def cancelorder(self, secID):
        keysgoodbye = []
        for key, order in self.onroad.items():
            if order.secID == secID:
                keysgoodbye.append(key)
                self.position.cancelrecord(order)
        for item in keysgoodbye:
            del self.onroad[item]

    def sendorder(self, onroadorder):
        self.cancelorder(onroadorder.secID)
        self.reforder += 1
        if (onroadorder.dir).upper() == "B":
            if self.position.LeftMoney >= onroadorder.price * onroadorder.vol:
                self.logger.info("{}, {}, {}, {}, {}, {}".format(onroadorder.date, onroadorder.secID, round(onroadorder.oriprice, 2),
                                                         round(onroadorder.price,2),
                                                         onroadorder.vol, onroadorder.dir))
                self.mainlogger.info("Sending Order : date : {}, secID : {}, oriprice : {},  price : {}, vol : {}, "
                      "dir : {}".format(onroadorder.date, onroadorder.secID, round(onroadorder.oriprice, 2), round(onroadorder.price, 2),
                                        onroadorder.vol, onroadorder.dir))
                self.onroad[self.reforder] = onroadorder
                self.position.sendrecord(onroadorder)
            else:
                self.mainlogger.info("Order {}, secID : {}, price : {}, vol : {}, "
                      "dir : {} cannot generate order for lacking of money.".format(self.reforder,onroadorder.secID,
                                                                                   round(onroadorder.price, 2), onroadorder.vol,
                                                                                   onroadorder.dir))
        elif (onroadorder.dir).upper() == "S":
            if self.position.Stocks[onroadorder.secID].sellable >= onroadorder.vol:
                self.logger.info("{}, {}, {}, {}, {}, {}".format(onroadorder.date, onroadorder.secID, round(onroadorder.oriprice, 2),
                                                         round(onroadorder.price,2),
                                                         onroadorder.vol, onroadorder.dir))
                self.mainlogger.info("Sending Order : date : {}, secID : {}, oriprice : {},  price : {}, vol : {}, "
                      "dir : {}".format(onroadorder.date, onroadorder.secID, round(onroadorder.oriprice, 2), round(onroadorder.price, 2),
                                        onroadorder.vol, onroadorder.dir))
                self.onroad[self.reforder] = onroadorder
                self.position.sendrecord(onroadorder)
            else:
                self.mainlogger.info("Order {}, secID : {}, price : {}, vol : {}, "
                      "dir : {} cannot generate order for no stock inventory.".format(self.reforder, onroadorder.secID,
                                                                                      round(onroadorder.price, 2), onroadorder.vol,
                                                                                      onroadorder.dir))
        else:
            raise Exception

if __name__ == "__main__":
    strategy1 = StrategyTemplate("./Strategy/Config/strategy1.json")