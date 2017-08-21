"""
Construct a strategy template, can be used to build more sophistcated strategy class
moduleaurther : Wang Wei <wangwei_aperion@163.com>
"""

import json
from Strategy.position import *
from abc import ABCMeta

class Strategy(ABCMeta):
    def __init__(self, path):
        if path is None:
            raise Exception
        else:
            self._pathfile = open(path, encoding="utf-8")
            self._strategystruct = json.load(self._pathfile)
            self._stock = self._strategystruct['stocklist']
            self._begin = self._strategystruct['starttime']
            self._end = self._strategystruct['endtime']

    def OnEvent(self, item):
        raise Exception




if __name__ == "__main__":
    strategy1 = Strategy("./Strategy/Config/strategy1.json")