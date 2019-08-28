#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
                            _ooOoo_  
                           o8888888o  
                           88" . "88  
                          (|  -_-  |)  
                           O\  =  /O  
                        ____/`---'\____  
                      .   ' \\| |// `.  
                       / \\||| : |||// \  
                     / _||||| -:- |||||- \  
                       | | \\\ - /// | |  
                     | \_| ''\---/'' | |  
                      \ .-\__ `-` ___/-. /  
                   ___`. .' /--.--\ `. . __  
                ."" '< `.___\_<|>_/___.' >'"".  
               | | : `- \`.;`\ _ /`;.`/ - ` : | |  
                 \ \ `-. \_ __\ /__ _/ .-` / /  
         ======`-.____`-.___\_____/___.-`____.-'======  
                            `=---='  
  
         .............................................  
                  佛祖镇楼                  BUG辟易  
          佛曰:  
                  写字楼里写字间，写字间里程序员；  
                  程序人员写程序，又拿程序换酒钱。  
                  酒醒只在网上坐，酒醉还来网下眠；  
                  酒醉酒醒日复日，网上网下年复年。  
                  但愿老死电脑间，不愿鞠躬老板前；  
                  奔驰宝马贵者趣，公交自行程序员。  
                  别人笑我忒疯癫，我笑自己命太贱；  
                  不见满街漂亮妹，哪个归得程序员？ 
'''
# @File  : connect_hbase.py
# @Author: huguangzhi
# @Drivce: Thinkpad E470
# @ContactEmail : huguangzhi@ucsdigital.com.com 
# @ContactPhone : 13121961510 
# @Date  : 2019-08-27 - 16:52
# @Desc  : 链接hbase的基本信息


import time
import json
import happybase



# def cli_conn():
#     # 创建一个scoket
#     transport = TSocket.TSocket(host=hbase_thrift_host,port=hbase_thrift_port)
#     # 包装一下scoket，让scoket环境在机器上，使用起来方便些。原始的socket太慢了
#     transport = TTransport.TBufferedTransport(transport)
#     # 遵循协议进行包装
#     protocol = TBinaryProtocol.TBinaryProtocol(transport)
#     # 创建客户端，并遵循协议编码
#     cli = Hbase.Client(protocol)
#     # 开启链接
#     transport.open()
#     return cli


def read_hbase(conn,tablename):
    table = conn.table(tablename)
    s = table.scan()
    dic = {}
    for key, value in s:
        dic[str(key,encoding="utf-8")] = {}
        for i in value:
            dic[str(key, encoding="utf-8")][str(i,encoding="utf-8")] = str(value[i],encoding="utf-8")
    return dic

def send_hbase_one(conn,table,data_dic):
    '''
    发送一行数据到hbase中，其中data_dic为当前的数据内容，
    :param conn: 链接器
    :param table: 表名，命名空间：表名
    :param data_dic: 数据格式{rowkey:{"列族：列名"："数据信息"……}}
    :return:
    '''
    table = conn.table(table)
    tab = table.batch()  # 创建batch
    for key in data_dic:
        tab.put(row=key,data=data_dic[key])
    tab.send()

if __name__ == '__main__':
    hbase_thrift_port = int(9090)
    hbase_thrift_host = str("192.168.30.115")
    hbase_table_name = str("nm1:spider_maoyan")
    conn = happybase.Connection(host=hbase_thrift_host, port=hbase_thrift_port)
    colume_fimaly = "cf1"
    rowkey = ""
    res = read_hbase(conn,hbase_table_name)
    print(res)
    # dic ={ '201908280313917':{'cinema_id': "16163",
    #                           'cinema_nm': '中影天幕国际影城',
    #                           'movie_dur': "110",
    #                           'movie_id': "1211270",
    #                           'movie_nm': '哪吒之魔童降世',
    #                           'movie_sc': '9.7',
    #                           'show_data': '2019-08-28 22:50',
    #                           'show_id': '201908280313917',
    #                           'show_lang': '国语',
    #                           'show_th': '2号厅',
    #                           'show_tp': '3D'
    #                       }}
    dic = {"201908280313917":{"path":"中影天幕国际影城"}}
    try:
        send_hbase_one(conn,hbase_table_name,dic)
    except:
        print("error")





















































