"""

moduleaurther : Wang Wei <wangwei_aperion@163.com>
"""

import json
from Strategy.record import *
from Strategy.position import *
from Dataloader.dispatcher import *
import pandas as pd

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

    def onbar(self, item):
        if item.volume == 0:
            pass
        else:
            ######## Time    Control     ##########
            if self.date is None:
                self.start()
                print("Begin backtesting : " + item.date)
                self.date = pd.to_datetime(item.date).date()
            if pd.to_datetime(item.date).date() > self.date:
                self.position.changedate()
                self.date = pd.to_datetime(item.date).date()
                print("Backtesting on : " + item.date)
            ######## Clear Untrade Order ##########
            self.clearorder(item)
            ######## User Code: Signal   ##########
            self.strategysignal(item)

    def strategysignal(self, item):
        pass

    def clearorder(self, item):
        for key,order in self.onroad.items():
            if order.price <= item.high and order.price >= item.low:
                print("Successful Transaction : secID : {}, price : {}, vol : {}, "
                      "dir : {}".format(order.secID, order.price, order.vol, order.dir))
                self.position.holdrecord(order.totransactionrecord())

    def sendorder(self, onroadorder):
        self.onroad.clear()
        self.reforder += 1
        if (onroadorder.dir).upper() == "B":
            if self.position.LeftMoney >= onroadorder.price * onroadorder.vol:
                print("Sending Order : secID : {}, price : {}, vol : {}, "
                      "dir : {}".format(onroadorder.secID, onroadorder.price, onroadorder.vol, onroadorder.dir))
                self.onroad.append({self.reforder : onroadorder})
            else:
                print("Order {}, secID : {}, price : {}, vol : {}, "
                      "dir : {} cannot generate order for lacking of money.".format(self.reforder,onroadorder.secID,
                                                                                   onroadorder.price, onroadorder.vol,
                                                                                   onroadorder.dir))
        elif (onroadorder.dir).upper() == "S":
            if self.position.Stocks[onroadorder.secID].sellable >= onroadorder.vol:
                print("Sending Order : secID : {}, price : {}, vol : {}, "
                      "dir : {}".format(onroadorder.secID, onroadorder.price, onroadorder.vol, onroadorder.dir))
                self.onroad.append({self.reforder : onroadorder})
            else:
                print("Order {}, secID : {}, price : {}, vol : {}, "
                      "dir : {} cannot generate order for no stock inventory.".format(self.reforder, onroadorder.secID,
                                                                                      onroadorder.price, onroadorder.vol,
                                                                                      onroadorder.dir))
        else:
            raise Exception

if __name__ == "__main__":
    strategy1 = StrategyTemplate("./Strategy/Config/strategy1.json")