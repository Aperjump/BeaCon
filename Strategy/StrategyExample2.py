"""
Test strategy, cited from other author
moduleaurther : vnpy
"""

from Strategy.strategy import *
from Strategy.record import *
import math
import talib
import numpy as np


class Stock(object):

    def __init__(self, secID, config):
        self.secID = secID
        self.config = config
        self.buffersize = self.config['buffersize']
        self.buffernum = 0
        # Set parameters
        self.atrLength = 22
        self.atrMaLength = 10
        self.rsiLength = 5
        self.rsiEntry = 16

        self.rsiBuy = 20 + self.rsiEntry
        self.rsiSell = 20 - self.rsiEntry

        self.closearray = []
        self.higharrary = []
        self.lowarrary = []
        self.atrarrary = []
        self.atrcount = 0
        self.atrbuffersize = 30

class Test2Strat(StrategyTemplate):

    def __init__(self, path = None):
        if path is None:
            path = "./Strategy/Config/strategyconfig2.json"
        StrategyTemplate.__init__(self, path = path)
        self.stocklist = {}
        for tempstock in self.stock:
            self.stocklist[tempstock] = Stock(tempstock, self.config)

    def strategysignal(self, item):
        singlestock = self.stocklist[item["code"]]
        if singlestock.buffernum < singlestock.buffersize:
            singlestock.closearray.append(item["close"])
            singlestock.higharrary.append(item["high"])
            singlestock.lowarrary.append(item["low"])
            singlestock.buffernum += 1
        else:
            singlestock.closearray.append(item["close"])
            singlestock.higharrary.append(item["high"])
            singlestock.lowarrary.append(item["low"])
            singlestock.closearray[0:singlestock.buffersize - 1] = singlestock.closearray[1:singlestock.buffersize]
            singlestock.higharrary[0:singlestock.buffersize - 1] = singlestock.higharrary[1:singlestock.buffersize]
            singlestock.lowarrary[0:singlestock.buffersize - 1] = singlestock.lowarrary[1:singlestock.buffersize]
            singlestock.atrvalue = talib.ATR(np.array(singlestock.higharrary, np.float64),
                                             np.array(singlestock.lowarrary, np.float64),
                                             np.array(singlestock.closearray, np.float64),
                                             np.array(singlestock.atrLength, np.float64))[-1]
            singlestock.atrcount += 1
            if singlestock.atrcount < singlestock.atrbuffersize:
                singlestock.atrarrary.append(singlestock.atrvalue)
            else:
                singlestock.atrarrary.append(singlestock.atrvalue)
                singlestock.atrarrary[0:singlestock.atrbuffersize - 1] = singlestock.atrarrary[1:singlestock.atrbuffersize]
                singlestock.atrMa = talib.MA(np.array(singlestock.atrarrary,np.float64),
                                             np.array(singlestock.atrMaLength, np.float64))[-1]
                singlestock.rsiValue = talib.RSI(np.array(singlestock.closearray, np.float64),
                                                 np.array(singlestock.rsiLength, np.float64))[-1]
                if singlestock.atrvalue > singlestock.atrMa:
                    if singlestock.rsiValue > singlestock.rsiBuy:
                        self.sendorder(OnRoadOrder(singlestock.secID, singlestock.closearray[-1] - 0.05, 300, "B", self.date))
                    elif singlestock.rsiValue < singlestock.rsiSell:
                        self.sendorder(OnRoadOrder(singlestock.secID, singlestock.closearray[-1] + 0.05, 300, "S", self.date))

if __name__ == "__main__":
    strategy1 = TestStrat("./Strategy/Config/strategy1.json")