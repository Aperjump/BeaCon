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
            self.config = json.load(open(path))
            self.stock = self.config['stocklist']
            # record orders which have not closed deal
            self.date = None
            self.reforder = 0
            self.onroad = {}
        self.logger = logging.getLogger("Main.strategy")
        self.mainlogger = logging.getLogger("Main")
        self.logger.addHandler(logging.FileHandler("./temp/sendorder.csv"))
        self.name = self.config['strategyname']

    def setdispatcher(self, dispatcher):
        self.dispatcher = dispatcher
        self.reg2dispatcher()

    def reg2dispatcher(self):
        for iterstock in self.stock:
            self.dispatcher.register(iterstock, self)

    def setaccount(self, position = None):
        if position is None:
            self.position = Position(self.config['initmoney'], commision = self.config['commision'],
                                     slipage = self.config['slipage'], name = self.name)
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
            self.position.calcposition(item)

    def strategysignal(self, item):
        pass

    def clearorder(self, item):
        keysgoodbye = []
        for key,order in self.onroad.items():
            if order.secID == item['code']:
                if order.price <= item["high"] and order.price >= item["low"]:
                    self.mainlogger.info("Successful Transaction : strategy : {}, secID : {}, price : {}, vol : {}, "
                          "dir : {}".format(self.name, order.secID, round(order.price, 2), order.vol, order.dir))
                    self.position.holdrecord(order.totransactionrecord(self.date))
                    keysgoodbye.append(key)
            else:
                pass
        for item in keysgoodbye:
            del self.onroad[item]

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
                self.logger.info("{}, {}, {}, {}, {}, {}, {}".format(self.name, onroadorder.date, onroadorder.secID, round(onroadorder.oriprice, 2),
                                                         round(onroadorder.price,2),
                                                         onroadorder.vol, onroadorder.dir))
                self.onroad[self.reforder] = onroadorder
                self.position.sendrecord(onroadorder)
            else:
                self.mainlogger.info("Strategyname : {}, Order {}, secID : {}, price : {}, vol : {}, "
                      "dir : {} cannot generate order for lacking of money.".format(self.name, self.reforder,onroadorder.secID,
                                                                                   round(onroadorder.price, 2), onroadorder.vol,
                                                                                   onroadorder.dir))
        elif (onroadorder.dir).upper() == "S":
            if (self.position.Stocks[onroadorder.secID].sellable >= onroadorder.vol) and (self.position.Stocks[onroadorder.secID].vol >= onroadorder.vol):
                self.logger.info("{}, {}, {}, {}, {}, {}, {}".format(self.name, onroadorder.date, onroadorder.secID, round(onroadorder.oriprice, 2),
                                                         round(onroadorder.price,2),
                                                         onroadorder.vol, onroadorder.dir))
                self.onroad[self.reforder] = onroadorder
                self.position.sendrecord(onroadorder)
            else:
                self.mainlogger.info("Strategyname : {}, Order {}, secID : {}, price : {}, vol : {}, "
                      "dir : {} cannot generate order for no stock inventory.".format(self.name, self.reforder, onroadorder.secID,
                                                                                      round(onroadorder.price, 2), onroadorder.vol,
                                                                                      onroadorder.dir))
        else:
            raise Exception

    def end(self):
        for iterstock in self.stock:
            self.cancelorder(iterstock)

if __name__ == "__main__":
    strategy1 = StrategyTemplate("./Strategy/Config/strategy1.json")