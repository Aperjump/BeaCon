"""
This class holds `money` transaction records, including InitMoney, StockValue, LeftMoney, TotalVal.
    TotalVal = StockValue + LeftMoney
Also, since in one day, investors can but stock multiple times, position should also hold records stock's
average holding costs for the convenience of individual stock revenue.
moduleaurther : Wang Wei <wangwei_aperion@163.com>
"""
class TransactionRecord(object):

    def __init__(self, secID, price, vol, direc):
        self.secID = secID
        self.price = price
        self.vol = vol
        # dir = 'B' means "Buy"
        # dir = 'S' means "Sell"
        self.dir = direc

    def topositionrecord(self):
        return PositionRecord(self.secID, self.price, self.vol, self.direc)

class PositionRecord(object):

    def __init__(self, secID, price, vol, direc):
        self.secID = secID
        self.avgprice = price
        self.vol = vol
        self.dir = direc

    def update(self, transrecord):
        if (transrecord.dir).upper() == "B":
            temptotalvol = self.vol + transrecord.vol
            self.avgprice = (self.avgprice * self.vol + transrecord.price * transrecord.vol) / temptotalvol
            self.vol = temptotalvol
        elif (transrecord.dir).upper() == "S":
            temptotalvol = self.vol - transrecord.vol
            try:
                assert temptotalvol > 0
            except AssertionError as e:
                print("Prohibit short stocks")
            # for log purpose
            earned = (self.avgprice - transrecord.price) * transrecord.vol
            self.avgprice = (self.avgprice * self.vol - transrecord.price  * transrecord.vol)  / temptotalvol

class Position(object):

    def __init__(self, initamount):
        # Set initial account
        self.InitMoney = initamount
        self.LeftMoney = initamount
        self.StockValue = 0
        self.TotalVal = initamount
        self.Stocks = {}

    def totalValadjust(self):
        self.TotalVal = self.LeftMoney + self.StockValue

    def holdrecord(self, transrecord):
        ## Account Value Change
        if (transrecord.dir).upper() == "B":
            self.LeftMoney = self.LeftMoney - (transrecord.price * transrecord.vol)
            self.StockValue = self.StockValue + (transrecord.price * transrecord.vol)
            self.totalValadjust()
        elif (transrecord.dir).upper() == "S":
            self.LeftMoney = self.LeftMoney + (transrecord.price * transrecord.vol)
            self.StockValue = self.StockValue - (transrecord.price * transrecord.vol)
            self.totalValadjust()
        # Stock Position Adjust
        if transrecord.secID in self.Stocks.keys():
            t_positionrecord = self.Stocks.get(transrecord.secID)
            t_positionrecord.update(transrecord)
        else:
            self.Stocks.__setitem__({transrecord.secID : transrecord.topositionrecord()})

