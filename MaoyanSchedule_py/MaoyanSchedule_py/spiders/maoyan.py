# -*- coding: utf-8 -*-
import scrapy
import requests
from MaoyanSchedule_py.items import MaoyanschedulePyItem
from scrapy.http import Request
import json

MaoyanschedulePyItem = MaoyanschedulePyItem()

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['www.maoyan.com']

    def getCityList(self):
        # 拿到城市列表信息
        cities_list = []
        city_list_url = "https://maoyan.com/ajax/cities"
        city_list = requests.get(city_list_url).json()
        for city_list_A in city_list["letterMap"]:
            cities_list.extend(city_list["letterMap"][city_list_A])
        return cities_list


    def getCienemaList(self, cityid:str):
        m = "http://m.maoyan.com/ajax/cinemaList?day=2019-08-22&offset=0&limit=999&cityId="
        cinema_list_url = m + cityid
        res = requests.get(cinema_list_url).json()
        try:
            return res["cinemas"]
        except:
            return []

    start_urls = []
    start_urls_model = "http://m.maoyan.com/ajax/cinemaDetail?cinemaId="


    for city in getCityList(1):
        cityid = city["id"]
        # print(cityid, city["nm"])
        cityname = city["nm"]
        cinemalist_onecity = getCienemaList(1, str(cityid))
        for cinemainfo in cinemalist_onecity:
            cinemaid = str(cinemainfo["id"])
            # print(cinemaid, cinemainfo["nm"])
            start_urls.append(start_urls_model+cinemaid)

    def parse(self, response):

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
                    # print(cinema_id,
                    #       cinema_nm,
                    #       movie_id,
                    #       movie_nm,
                    #       movie_sc,
                    #       movie_dur,
                    #       show_data,
                    #       show_tm,
                    #       show_lang,
                    #       show_seqNo,
                    #       show_th,
                    #       show_tp
                    #       )









