import pymongo
import pandas as pd
import json
import os
import zipfile
import io

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
        for iterdirfiles in self.dirfiles:
            print("current month: " + iterdirfiles)
            datesfiles = os.listdir(iterdirfiles)
            length = len(datesfiles)
            n = 0
            for iterdatesfiles in datesfiles:
                currentdayfiles = zipfile.ZipFile("./"+ iterdirfiles + "/" + iterdatesfiles, 'r')
                for filename in currentdayfiles.namelist():
                    print("reading file: " + filename)
                    data = currentdayfiles.read(filename)
                    filename = filename[:-4]
                    filenamesplit = filename.split(" ")
                    self._docu = self._col[filenamesplit[1]]
                    datastrio = io.StringIO(data.decode("gb2312"))
                    junkword = next(datastrio)
                    data = pd.read_csv(datastrio)
                    data.columns = ['code','date','open','high', 'low', 'close', 'volume', 'transac', 'trradenum']
                    tempdata = data[['code','date', 'open', 'high', 'low', 'close', 'volume']]
                    pd.options.mode.chained_assignment = None
                    tempdata['code'] = tempdata['code'].map(lambda x : x[2:])
                    self._docu.insert_many(json.loads(tempdata.to_json(orient='records')))
                    print(filename + " finish.")
                n += 1
                print(str(round((n / length) * 100,2)) + "%")

    def initmongo(self):
        # Connect to Mongodb
        self._client = pymongo.MongoClient(self.config['mongodburl'])
        self._col = self._client[self.config['mongocollection']]
        self._docu = self._col[self.config['mongodocument']]

if __name__ == "__main__":
    storage = StorageFromDist("E://QuantFrameWork//BeaCon//Storage//NewDB//configmin.json")
    storage.loadmin()
   #storage = StorageFromDist()
   # storage.load()