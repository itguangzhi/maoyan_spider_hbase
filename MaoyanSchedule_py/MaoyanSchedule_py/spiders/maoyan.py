# -*- coding: utf-8 -*-
import scrapy
import scrapy.core.scheduler
from scrapy.log import *
from MaoyanSchedule_py.items import MaoyanschedulePyItem
from scrapy.http import Request
import json



import time
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
            print("##  load " + str(city_list["letterMap"][city_list_A]), end="")
            for city in city_list["letterMap"][city_list_A]:
                cityid = city["id"]
                cityname = city["nm"]
                print("## use " + cityname,end="")
                cinema_list_url = "http://m.maoyan.com/ajax/cinemaList?day=2019-08-22&offset=0&limit=999&cityId="
                yield Request(url=cinema_list_url+str(cityid),
                              dont_filter=True,
                              callback=self.cinemalist_parse,
                              meta={"city_id":cityid,"city_nm":cityname}
                              )


    def cinemalist_parse(self,response):
        try:
            cinemalist_onecity = json.loads(response.text)["cinemas"]
            for cinemainfo in cinemalist_onecity:
                cinemaid = str(cinemainfo["id"])
                cinema_url = "http://m.maoyan.com/ajax/cinemaDetail?cinemaId="
                yield Request(url=cinema_url+cinemaid,
                              callback=self.parse_detail,
                              dont_filter=True,
                              meta={"city_id":response.meta["city_id"],
                                    "city_nm":response.meta["city_nm"]}
                              )
        except Exception as e:
            print("城市 "+ response.meta["city_nm"] +" 影院列表解析错误，地址：",str(response.url))
            print(e)


    def parse_detail(self, response):
        try:
            res = json.loads(response.text)["showData"]
            cinema_id = res["cinemaId"]
            cinema_nm = res["cinemaName"]
            movies_info = res["movies"]
            schedul_data = {}
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
                        MaoyanschedulePyItem["show_data"] = show_data + " " + show_tm
                        MaoyanschedulePyItem["movie_id"] = str(movie_id)
                        MaoyanschedulePyItem["movie_nm"] = movie_nm
                        MaoyanschedulePyItem["movie_sc"] = movie_sc
                        MaoyanschedulePyItem["movie_dur"] = str(movie_dur)
                        MaoyanschedulePyItem["cinema_id"] = str(cinema_id)
                        MaoyanschedulePyItem["cinema_nm"] = cinema_nm
                        MaoyanschedulePyItem["spider_url"] = response.url
                        MaoyanschedulePyItem["city_id"] = str(response.meta["city_id"])
                        MaoyanschedulePyItem["city_nm"] = response.meta["city_nm"]
                        MaoyanschedulePyItem["spider_time"] = str(time.time())

                        datas = {
                            str(cinema_id) + "-" + str(movie_id) + "-" + str(show_seqNo): {
                                "cf1:cinema_id": str(cinema_id),
                                "cf1:cinema_nm": str(cinema_nm),
                                "cf1:movie_dur": str(movie_dur),
                                "cf1:movie_id": str(movie_id),
                                "cf1:movie_nm": str(movie_nm),
                                "cf1:movie_sc": str(movie_sc),
                                "cf1:show_data": str(show_data),
                                "cf1:show_lang": str(show_lang),
                                "cf1:show_th": str(show_th),
                                "cf1:spider_url": str(response.url),
                                "cf1:show_tp": str(show_tp),
                                "cf1:city_id": str(response.meta["city_id"]),
                                "cf1:city_nm": str(response.meta["city_nm"]),
                                "cf1:spider_time": str(time.time()),
                                "cf1:show_id": str(show_seqNo),

                            },
                        }
                        schedul_data.update(datas)

                        yield Request(
                            url="http://m.maoyan.com/movie/" + str(cinema_id),
                            dont_filter=False,
                            callback=self.movie_parse
                        )



            MaoyanschedulePyItem["schedul_item"] = schedul_data
            yield MaoyanschedulePyItem

            # yield Request(
            #     url=response.url,
            #     meta={"city_id": response.meta["city_id"],
            #           "city_nm": response.meta["city_nm"]},
            #     dont_filter=True,
            #     callback=self.parse_detail
            # )
        except Exception as e:
            print(response.url,e)


    def movie_parse(self,response):

        movie_content = response.xpath('//div[@class="text-expander-content"]/p/text()').extract_first("")
        page_img = '//li[@class="stage-img-container"]/a/img/@src'
        movie_image = response.xpath(page_img)
        image_url_list = ["http:" + i.split("@")[0] for i in movie_image]
        movie_name = response.xpath('/html/head/title/text()').extract_first()
        movie_category = response.xpath('//div[@class="movie-category"]/span/text()').extract_first()
        MaoyanschedulePyItem["image_url_list"] = image_url_list
        MaoyanschedulePyItem["movie_name"] = movie_name
        MaoyanschedulePyItem["movie_category"] = movie_category
        MaoyanschedulePyItem["movie_content"] = movie_content
































