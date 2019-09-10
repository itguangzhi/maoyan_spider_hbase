# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import happybase
from MaoyanSchedule_py.utils.connect_hbase import *


class MaoyanschedulePyPipeline(object):
    def process_item(self, item, spider):
        return item



class MaoyanscheduleHbasePipeline(object):
    hbase_thrift_port = int(9090)
    hbase_thrift_host = str("192.168.30.115")
    hbase_table_name = str("nm1:spider_maoyan")

    def __init__(self):
        self.conn = happybase.Connection(host=self.hbase_thrift_host,
                                         port=self.hbase_thrift_port)
        self.connp = happybase.ConnectionPool(host=self.hbase_thrift_host,
                                            port=self.hbase_thrift_port,
                                             size=1000)

        self.cf = "cf1"


    def process_item(self, item, spider):
        # {rowkey: {"列族：列名"："数据信息"……}}

        insert_data_list = item["schedul_item"]

        with self.connp.connection() as conn:
            send_hbase_one(conn, self.hbase_table_name, insert_data_list)
            # send_hbase_one(conn, self.hbase_table_name, insert_data)
        return item

