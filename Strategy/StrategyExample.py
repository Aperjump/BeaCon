"""
Test strategy, cited from other author
moduleaurther : vnpy
"""

from Strategy.strategy import *
from collections import deque
import math
import talib

class Stock(object):

    def __init__(self, secID):
        self.secID = secID
        self.buffersize = self.config['buffersize']
        self.buffernum = 0
        # Set parameters
        self.atrLength = 22
        self.atrMaLength = 10
        self.rsiLength = 5
        self.rsiEntry = 16

        self.rsiBuy = 50 + self.rsiEntry
        self.rsiSell = 50 - self.rsiEntry

        self.closearray = []
        self.higharrary = []
        self.lowarrary = []
        self.atrarrary = []
        self.atrcount = 0
        self.atrbuffersize = 100

class TestStrat(StrategyTemplate):

    def __init__(self, path = None):
        if path is None:
            path = "./Strategy/Config/strategyconfig.json"
        StrategyTemplate.__init__(self, path = path)
        self.stocklist = {}
        for tempstock in self.stock:
            self.stocklist[tempstock] = Stock(tempstock)

    def strategysignal(self, item):
        singlestock = self.stocklist[item.code]
        if singlestock.buffernum < singlestock.buffersize:
            singlestock.closearray.append(item)
            singlestock.higharrary.append(item)
            singlestock.lowarrary.append(item)
            singlestock.buffernum += 1
        else:
            singlestock.closearray.append(item)
            singlestock.higharrary.append(item)
            singlestock.lowarrary.append(item)
            singlestock.closearray[0:singlestock.buffersize - 1] = singlestock.closearray[1:singlestock.buffersize]
            singlestock.higharrary[0:singlestock.buffersize - 1] = singlestock.higharrary[1:singlestock.buffersize]
            singlestock.lowarrary[0:singlestock.buffersize - 1] = singlestock.lowarrary[1:singlestock.buffersize]
            singlestock.atrvalue = talib.ATR(singlestock.higharrary,
                                             singlestock.lowarrary,
                                             singlestock.closearray,
                                             singlestock.atrLength)[-1]
            singlestock.atrcount += 1
            if singlestock.atrcount < singlestock.atrbuffersize:
                singlestock.atrarrary.append(singlestock.atrvalue)
            else:
                singlestock.atrarrary.append(singlestock.atrvalue)
                singlestock.atrarrary[0:singlestock.atrbuffersize - 1] = singlestock.atrarrary[1:singlestock.atrbuffersize]
                singlestock.atrMa = talib.MA(singlestock.atrarrary,
                                             singlestock.atrMaLength)[-1]
                singlestock.rsiValue = talib.RSI(singlestock.closearray,
                                                 singlestock.rsiLength)[-1]
                if singlestock.atrvalue > singlestock.atrMa:
                    if singlestock.rsiValue > singlestock.rsiBuy:
                        singlestock.sendorder(singlestock.secID, 300, singlestock.closearray[-1] + 0.02, "B")
                    elif singlestock.rsiValue < singlestock.rsiSell:
                        singlestock.sendorder(singlestock.secID, 300, singlestock.closearray[-1] - 0.02, "S")

if __name__ == "__main__":
    strategy1 = TestStrat("./Strategy/Config/strategy1.json")