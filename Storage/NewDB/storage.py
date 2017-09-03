import pymongo
import pandas as pd
import json
import os

class StorageFromDist(object):

    def __init__(self, path = None):
        if path is None:
            path = "./config.json"
        self.config = json.load(open(path))
        self.initmongo()

    def load(self):
        os.chdir(self.config['DataDirectory'])
        self.dirfiles = os.listdir()
        length = len(self.dirfiles)
        n = 0
        for file in self.dirfiles:
            tempdata = pd.read_csv(file)
            tempdata = tempdata[['date','open','high','low','close','volume','adjust_price']]
            # file : "sh600060.csv"
            tempdata['code'] = file[2:-4]
            self._docu.insert_many(json.loads(tempdata.to_json(orient='records')))
            n += 1
            print(file[2:-4] + " finish!  {}%".format(round((n / length) * 100,2)))

    def loadmin(self):
        os.chdir(self.config['DataDirectory'])
        self.dirfiles = os.listdir()

    def initmongo(self):
        # Connect to Mongodb
        self._client = pymongo.MongoClient(self.config['mongodburl'])
        self._col = self._client[self.config['mongocollection']]
        self._docu = self._col[self.config['mongodocument']]

if __name__ == "__main__":
    storage = StorageFromDist()
    storage.load()