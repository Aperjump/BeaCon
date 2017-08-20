"""

"""

import json

class strategy:
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
        print(item)

if __name__ == "__main__":
    strategy1 = strategy("./Strategy/Config/strategy1.json")