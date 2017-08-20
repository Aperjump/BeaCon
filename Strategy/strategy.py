"""

"""

class strategy(object):
    def __init__(self):
        self._stock = '600060'
        self._begin = "2014-01-01"
        self._end = "2016-04-05"

    def OnEvent(self, item):
        print(item)