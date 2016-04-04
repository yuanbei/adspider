# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from os import path
from pydispatch import dispatcher
from pylib import db
from scrapy import signals
from sql_constants import *
import sqlite3


class SQLiteStorePipeline(object):
    filename = 'ads_profile.sqlite'

    def __init__(self):
        self.conn = None
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)

    def process_item(self, item, spider):
        self.conn.execute(INSERT_ITEM_SQLITE,
                          (item['ads_target_url'],
                           item['ads_content_url'],
                           item['ads_present_mode'],
                           item['ads_host'],
                           item['ads_target_domain'],
                           item['ads_host_domain']))
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
        conn.execute(CREATE_ADS_PROFILE_TABLE_SQLITE)
        conn.commit()
        return conn


class MySQLStorePipeline(object):

    def __init__(self, dbspec):
        self.conn = None
        self.dbspec = dbspec
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(dbspec=crawler.settings.get('MYSQL_DBSPEC'))

    def process_item(self, item, spider):
        if self.conn is not None:
            self.conn.Execute(INSERT_ITEM_MYSQL,
                              {
                                  'ads_target_url': item['ads_target_url'],
                                  'ads_content_url': item['ads_content_url'],
                                  'ads_present_mode': item['ads_present_mode'],
                                  'ads_host': item['ads_host'],
                                  'ads_target_domain': item['ads_target_domain'],
                                  'ads_host_domain': item['ads_host_domain']
                              })
        return item

    def initialize(self):
        self.conn = db.Connect(self.dbspec)
        if self.conn is not None:
            self.create_ads_profile_table()
            self.create_ads_refer_graph_table()
            self.create_and_update_refer_graph_trigger()

    def finalize(self):
        if self.conn is not None:
            self.conn.Close()
            self.conn = None

    def create_ads_profile_table(self):
        self.conn.Execute(CREATE_ADS_PROFILE_TABLE_MYSQL)

    def create_ads_refer_graph_table(self):
        self.conn.Execute(CREATE_ADS_REFER_GRAPH_MYSQL)

    def create_and_update_refer_graph_trigger(self):
        self.conn.Execute(CREATE_TRIGGER_MYSQL)
