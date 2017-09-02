"""
Various Transaction Data
moduleaurther : Wang Wei <wangwei_aperion@163.com>
"""
class PositionRecord(object):

    def __init__(self, secID, price, vol, direc):
        self.secID = secID
        self.avgprice = price
        self.vol = vol
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
            temptotalvol = self.vol - transrecord.vol
            # for log purpose
            earned = (transrecord.price - self.avgprice) * transrecord.vol
            self.avgprice = (self.avgprice * self.vol - transrecord.price * transrecord.vol) / temptotalvol
        else:
            raise Exception

class TransactionRecord(object):

    def __init__(self, secID, price,oriprice, vol, direc, date):
        self.secID = secID
        self.price = price
        self.vol = vol
        # dir = 'B' means "Buy"
        # dir = 'S' means "Sell"
        self.dir = direc
        self.oriprice = oriprice
        self.date = date

    def topositionrecord(self):
        return PositionRecord(self.secID, self.price, self.vol, self.dir)

class OnRoadOrder(object):

    def __init__(self, secID, price, vol, direc, date):
        self.secID = secID
        self.price = price
        self.vol = vol
        # dir = 'B' means "Buy"
        # dir = 'S' means "Sell"
        self.dir = direc
        # self.count = 0
        #self.alive = True
        self.oriprice = price
        self.date = date

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
        self.oriprice = 0
        self.date = None
    def totransactionrecord(self, date):
        return TransactionRecord(self.secID, self.price,self.oriprice, self.vol, self.dir, date)

    def adjustprice(self, commision=None, slipage=None):
        if (self.dir).upper() == "B":
            self.price = round(self.price * (1 + slipage) * (1 + commision), 2)
        elif (self.dir).upper() == "S":
            self.price = round(self.price * (1 - slipage) * (1 - commision), 2)
        else:
            raise Exception
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