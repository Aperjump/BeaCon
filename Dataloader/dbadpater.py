"""
Each atomicdispatcher connects one instance of dbadapter, which encapsulate connection to database,
adapting it to an iterater. Through iterating the database, dbadapter get one namedtuple at a time.
moduleaurther : Wang Wei <wangwei_aperion@163.com>
"""

import pymongo
import json
class dbadapter(object):

    def __init__(self, mongconct):
        self._connection = mongconct
