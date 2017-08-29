"""
Used for updating new stock trading data, stock config file use stocknames.json.
moduleaurther : Wang Wei <wangwei_aperion@163.com>
"""

import tushare as ts
import pandas as pd
import pymongo
import json
import time
from Storage.storage import UpdateConfig

if __name__ == "__main__":
    update = UpdateConfig()
    update.initmongo()
    update.insert()



