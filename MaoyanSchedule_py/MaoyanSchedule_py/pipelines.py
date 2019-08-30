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
        insert_data = {
            str(item["show_id"]):{
                self.cf + ":cinema_id" : item["cinema_id"],
                self.cf + ":cinema_nm" : item["cinema_nm"],
                self.cf + ":movie_dur" : item["movie_dur"],
                self.cf + ":movie_id" : item["movie_id"],
                self.cf + ":movie_nm" : item["movie_nm"],
                self.cf + ":movie_sc" : item["movie_sc"],
                self.cf + ":show_data" : item["show_data"],
                self.cf + ":show_lang" : item["show_lang"],
                self.cf + ":show_th" : item["show_th"],
                self.cf + ":spider_url" : item["spider_url"],
                self.cf + ":show_tp" : item["show_tp"],
                self.cf + ":city_id" : item["city_id"],
                self.cf + ":city_nm" : item["city_nm"],
                self.cf + ":spider_time" : item["spider_time"],
            }
        }

        insert_data_list = item["schedul_item"]

        with self.connp.connection() as conn:
            send_hbase_one(conn, self.hbase_table_name, insert_data_list)
            # send_hbase_one(conn, self.hbase_table_name, insert_data)
        return item

