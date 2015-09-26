#coding:utf8

"""
database.py
~~~~~~~~~~~~~

该模块提供爬虫所需的sqlite数据库的创建、连接、断开，以及数据的存储功能。
"""

import sqlite3

class Database(object):
    def __init__(self, dbFile):
        try:
            self.conn = sqlite3.connect(dbFile, isolation_level=None, check_same_thread = False) #让它自动commit，效率也有所提升. 多线程共用
            self.conn.execute('''CREATE TABLE IF NOT EXISTS
                            AdsProfile (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            adsURL TEXT, 
                            adsTargetURL TEXT,
                            referURL TEXT)''')
        except Exception, e:
            self.conn = None

    def isConn(self):
        if self.conn:
            return True
        else:
            return False

    def saveData(self, adsURL, adsTargetURL, referURL):
        if self.conn:
            sql='''INSERT INTO AdsProfile (adsURL, adsTargetURL, referURL) VALUES (?, ?, ?);'''
            self.conn.execute(sql, (adsURL, adsTargetURL, referURL) )
        else :
            raise sqlite3.OperationalError,'Database is not connected. Can not save Data!'

    def close(self):
        if self.conn:
            self.conn.close()
        else :
            raise sqlite3.OperationalError, 'Database is not connected.'
