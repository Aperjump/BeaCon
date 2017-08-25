"""
MA Strategy Test:
Rule:
If MA(5) upcross MA(10) generate buy signal;
if MA(5) downcross MA(10) generate sell signal.

moduleaurther : Wang Wei <wangwei_aperion@163.com>
"""

from Strategy.strategy import *
from collections import deque
import math

class TestStrat(Strategy):

    def __init__(self, path = None):
        if path is None:
            path = "./Strategy/Config/strategy1.json"
        Strategy.__init__(self, path = path)
        self.temporder = OnRoadOrder()
        # Set parameters
        self.count = 0
        self.para1 = self._strategystruct["length1"]
        self.para2 = self._strategystruct["length2"]
        self.length1 = deque()
        self.length2 = deque()

    # help function
    def paraminit(self, item):
        if self.count <= self.para1:
            self.length1.append(item.close)
            self.length2.append(item.close)
        elif self.count > self.para1 and self.count <= self.para2:
            self.updateslow(item)
            self.length2.append(item.close)

    def updateslow(self, item):
        self.length1.pop()
        self.length1.append(item.close)
        self.MA1 = math.mean(self.length1)

    def updatelong(self, item):
        self.length2.pop()
        self.length2.append(item.close)
        self.MA2 = math.mean(self.length2)

    def OnEvent(self, item):
        self.count += 1
        self.onroad.checktrade(item)
        if self.count <= self.para2:
            self.paraminit(item)
        else:
            self.updateslow(item)
            self.updatelong(item)
        if (self.MA1 > self.MA2):
            self.temporder = self.temporder.build(self._stock, "op", "all", "B")
            self.sendorder(self.temporder)




if __name__ == "__main__":
    strategy1 = TestStrat("./Strategy/Config/strategy1.json")