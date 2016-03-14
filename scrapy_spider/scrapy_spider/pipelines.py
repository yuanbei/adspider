# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
from os import path

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

INSERT_ITEM_SQL = '''INSERT INTO AdsProfile
                     (ads_target_url,
                      ads_content_url,
                      ads_present_mode,
                      ads_host) VALUES(?,?,?,?)'''
CREATE_ADS_PROFILE_TABLE_SQL = '''CREATE TABLE IF NOT EXISTS AdsProfile (
                                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                                  ads_target_url TEXT,
                                  ads_content_url TEXT,
                                  ads_present_mode TEXT,
                                  ads_host TEXT)'''


class SQLiteStorePipeline(object):
    filename = 'ads_profile.sqlite'

    def __init__(self):
        self.conn = None
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)

    def process_item(self, item, spider):
        self.conn.execute(INSERT_ITEM_SQL,
                          (item['ads_target_url'],
                           item['ads_content_url'],
                           item['ads_present_mode'],
                           item['ads_host']))
        return item

    def initialize(self):
        if path.exists(self.filename):
            self.conn = sqlite3.connect(self.filename)
        else:
            self.conn = self.create_table(self.filename)

    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    def create_table(self, filename):
        conn = sqlite3.connect(filename)
        conn.execute(CREATE_ADS_PROFILE_TABLE_SQL)
        conn.commit()
        return conn
