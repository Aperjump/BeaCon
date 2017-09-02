"""
Various Transaction Data
moduleaurther : Wang Wei <wangwei_aperion@163.com>
"""

class PositionRecord(object):

    def __init__(self, secID, price, vol, direc):
        self.secID = secID
        self.avgprice = float(price)
        self.vol = float(vol)
        self.dir = direc
        self.sellable = 0

    def __repr__(self):
        return "secID : {}, avgprice : {}, vol : {}, dir : {}, sellable : {}".format(self.secID,
                                                                                    self.avgprice,
                                                                                    self.vol,
                                                                                    self.dir,
                                                                                    self.sellable)

    def __str__(self):
        return "secID : {}, avgprice : {}, vol : {}, dir : {}, sellable : {}".format(self.secID,
                                                                                    self.avgprice,
                                                                                    self.vol,
                                                                                    self.dir,
                                                                                    self.sellable)
    def update(self, transrecord):
        if (transrecord.dir).upper() == "B":
            temptotalvol = self.vol + transrecord.vol
            self.avgprice = (self.avgprice * self.vol + transrecord.price * transrecord.vol) / temptotalvol
            self.vol = temptotalvol
        elif (transrecord.dir).upper() == "S":
            temptotalvol = self.sellable - transrecord.vol
            try:
                assert temptotalvol > 0
            except AssertionError as e:
                print("Prohibit short stocks")
            # for log purpose
            earned = (self.avgprice - transrecord.price) * transrecord.vol
            self.avgprice = (self.avgprice * self.vol - transrecord.price * transrecord.vol) / temptotalvol
        else:
            raise Exception

class TransactionRecord(object):

    def __init__(self, secID, price, vol, direc):
        self.secID = secID
        self.price = float(price)
        self.vol = float(vol)
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

class OnRoadOrder(object):

    def __init__(self, secID, price, vol, direc):
        self.secID = secID
        self.price = float(price)
        self.vol = float(vol)
        # dir = 'B' means "Buy"
        # dir = 'S' means "Sell"
        self.dir = direc
        # self.count = 0
        #self.alive = True

    def __repr__(self):
        return "SecID : {}, price : {}, vol : {}, direction : {}".format(self.secID, self.price,
                                                                        self.vol, self.dir)

    def destruct(self):
        self.secID = "000000"
        self.price = 10
        self.vol = 100
        self.dir = "B"
        # self.count = 0
        # self.alive = False

    def totransactionrecord(self):
        return TransactionRecord(self.secID, self.price, self.vol, self.dir)
"""
DEPRECATED
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
"""