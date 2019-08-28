# -*- coding: utf-8 -*-
import json
from scrapy.http import Request
import scrapy


class MaoyanSchedulSpider(scrapy.Spider):
    name = 'maoyan_schedul'
    allowed_domains = ['www.maoyan.com']
    # start_urls = ['maoyan.com/ajax/cities/']
    start_urls = ['http://m.maoyan.com/ajax/cinemaDetail?cinemaId=154',]

    def parse(self, response):
        schedul_res = json.loads(response.text)["showData"]
        cinema_id = schedul_res["cinemaId"]
        cinema_nm = schedul_res["cinemaName"]
        movies_info = schedul_res["movies"]
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
                    print(show_th)






    #     city_res = json.loads(response.text)
    #     for city_list_A in city_res["letterMap"]:
    #         for cities in city_res["letterMap"][city_list_A]:
    #             city_id = str(cities["id"])
    #             city_cinemas_model = r"http://m.maoyan.com/ajax/cinemaList?day=2019-08-23&offset=0&limit=999&cityId="
    #             Request(
    #                 url=city_cinemas_model+city_id,
    #                 meta={"city": cities},
    #                 callback=self.parse_getCienemaList,
    #                 dont_filter=True)
    #             print(cities["nm"])
    #
    # def parse_getCienemaList(self, response):
    #     cinemas_res = json.loads(response.text)
    #     if len(cinemas_res["cinemas"]) != 0:
    #         for cinema in cinemas_res["cinemas"]:
    #             cinema_url_model = r"http://m.maoyan.com/ajax/cinemaDetail?cinemaId="
    #             Request(
    #                 url=cinema_url_model+str(cinema["id"]),
    #                 meta={"cinema": cinema},
    #                 callback=self.parse_getSchedul,
    #                 dont_filter = True
    #             )
    #             print(cinema["nm"])
    #
    # def parse_getSchedul(self, response):
    #     schedul_res = json.loads(response.text)["showData"]
    #     cinema_id = schedul_res["cinemaId"]
    #     cinema_nm = schedul_res["cinemaName"]
    #     movies_info = schedul_res["movies"]
    #     for mov in movies_info:
    #         movie_id = mov["id"]
    #         movie_nm = mov["nm"]
    #         movie_sc = mov["sc"]
    #         movie_dur = mov["dur"]  # 放映时长
    #         for movie_show in mov["shows"]:
    #             show_data = movie_show["showDate"]  # 放映时间
    #             for show_list in movie_show["plist"]:
    #                 show_lang = show_list["lang"]  # 放映语言
    #                 show_seqNo = show_list["seqNo"]  # 放映编码
    #                 show_th = show_list["th"]  # 放映影厅名
    #                 show_tm = show_list["tm"]  # 放映开始时间
    #                 show_tp = show_list["tp"]  # 放映类型 3D 2D