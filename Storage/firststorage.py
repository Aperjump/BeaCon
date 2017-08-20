"""
Used for database init.
moduleaurther : Wang Wei <wangwei_aperion@163.com>
"""

import tushare as ts
import pandas as pd
import pymongo
import json
import time
from Storage.storage import StorageConfig

if __name__ == "__main__":
    storage = StorageConfig()
    storage.initmongo()
    storage.insert()
