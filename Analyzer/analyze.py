"""
Analyze strategy performance
moduleaurther : Wang Wei <wangwei_aperion@163.com>
"""
import pandas as pd
import numpy as np
import json
import pymongo

class Analyzer(object):

    def __init__(self, path = None):
        if path is None:
            self.path = "../Strategy/temp/position.csv"
        else:
            self.path = path
        self.loadrecord()

    def loadrecord(self):
        self.avgpricerecord = pd.read_csv(self.path, header=None, names=["strategy","time", "stock","currentprice", "avgprice", "vol", "earn"])
        self.avgpricerecord['stock'] = self.avgpricerecord.apply(lambda x: str(x).zfill(6))
        self.money = pd.read_csv("../Strategy/temp/moneyrecord.csv", header=None,
                                     names=["strategy",'time', 'left', 'stockvalue', 'whole'])
        # self.combine = pd.merge(self.avgpricerecord, self.leftmoney, how="left", on="time")

if __name__ == "__main__":
    data = pd.read_csv("E:/QuantFrameWork/BeaCon/Strategy/temp/position.csv",header = None, names = ["strategy","time", "stock","currentprice", "avgprice", "vol", "earn"])
    data['stock'] = data['stock'].apply(lambda x : str(x).zfill(6))
    money = pd.read_csv("E:/QuantFrameWork/BeaCon/Strategy/temp/moneyrecord.csv",header = None, names = ["strategy",'time','left','stockvalue','whole'])
    test1 = money[money['strategy'] == 'test']
    test2 = money[money['strategy'] == 'test2']
    test1 = test1[(test1['time'] >= ' 2015-08-01') & (test1['time'] <= ' 2017-02-03')]
    test1.plot(x = 'time', y = 'whole')
