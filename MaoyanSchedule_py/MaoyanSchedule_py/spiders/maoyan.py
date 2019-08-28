# -*- coding: utf-8 -*-
import scrapy
import requests
from MaoyanSchedule_py.items import MaoyanschedulePyItem
from scrapy.http import Request
import json
import threading
MaoyanschedulePyItem = MaoyanschedulePyItem()


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['www.maoyan.com']
    start_urls = ["https://maoyan.com/ajax/cities"]
    start_urls_model = "http://m.maoyan.com/ajax/cinemaDetail?cinemaId="


    def parse(self, response):
        cities_list = []
        city_list = json.loads(response.text)
        for city_list_A in city_list["letterMap"]:
            cities_list.extend(city_list["letterMap"][city_list_A])
            print("load " + str(city_list["letterMap"][city_list_A]))
            for city in city_list["letterMap"][city_list_A]:
                cityid = city["id"]
                cityname = city["nm"]
                print("use " + cityname)
                cinema_list_url = "http://m.maoyan.com/ajax/cinemaList?day=2019-08-22&offset=0&limit=999&cityId="
                yield Request(url=cinema_list_url+str(cityid),dont_filter=True,callback=self.cinemalist_parse)


    def cinemalist_parse(self,response):
        try:
            cinemalist_onecity = json.loads(response.text)["cinemas"]
            for cinemainfo in cinemalist_onecity:
                cinemaid = str(cinemainfo["id"])
                cinema_url = "http://m.maoyan.com/ajax/cinemaDetail?cinemaId="
                yield Request(url=cinema_url+cinemaid,callback=self.parse_detail,dont_filter=True)
        except:
            print("城市影院解析错误",str(json.load(response.text)))

    def parse_detail(self, response):
        res = json.loads(response.text)["showData"]
        cinema_id = res["cinemaId"]
        cinema_nm = res["cinemaName"]
        movies_info = res["movies"]
        for mov in movies_info:
            movie_id = mov["id"]
            movie_nm = mov["nm"]
            movie_sc = mov["sc"]
            movie_dur = mov["dur"]  # 放映时长
            for movie_show in mov["shows"]:
                show_data = movie_show["showDate"]  # 放映时间
                for show_list in movie_show["plist"]:
                    show_lang = show_list["lang"]  # 放映语言
                    show_seqNo = show_list["seqNo"]  # 放映编码
                    show_th = show_list["th"]  # 放映影厅名
                    show_tm = show_list["tm"]  # 放映开始时间
                    show_tp = show_list["tp"]  # 放映类型 3D 2D
                    MaoyanschedulePyItem["show_id"] = show_seqNo
                    MaoyanschedulePyItem["show_lang"] = show_lang
                    MaoyanschedulePyItem["show_th"] = show_th
                    MaoyanschedulePyItem["show_tp"] = show_tp
                    MaoyanschedulePyItem["show_data"] = show_data+" "+ show_tm
                    MaoyanschedulePyItem["movie_id"] = str(movie_id)
                    MaoyanschedulePyItem["movie_nm"] = movie_nm
                    MaoyanschedulePyItem["movie_sc"] = movie_sc
                    MaoyanschedulePyItem["movie_dur"] = str(movie_dur)
                    MaoyanschedulePyItem["cinema_id"] = str(cinema_id)
                    MaoyanschedulePyItem["cinema_nm"] = cinema_nm
                    MaoyanschedulePyItem["spider_url"] = response.url

                    yield  MaoyanschedulePyItem

