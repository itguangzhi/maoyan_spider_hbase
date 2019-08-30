# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MaoyanschedulePyItem(scrapy.Item):
    # define the fields for your item here like:
    spider_url= scrapy.Field()
    show_id = scrapy.Field()
    show_lang = scrapy.Field()
    show_th = scrapy.Field()
    show_tp = scrapy.Field()
    show_data = scrapy.Field()
    movie_id = scrapy.Field()
    movie_nm = scrapy.Field()
    movie_sc = scrapy.Field()
    movie_dur = scrapy.Field()
    cinema_id = scrapy.Field()
    cinema_nm = scrapy.Field()
    city_id = scrapy.Field()
    city_nm = scrapy.Field()
    spider_time = scrapy.Field()

    # 影片相关的信息内容
    image_url_list = scrapy.Field()
    movie_name = scrapy.Field()
    movie_category = scrapy.Field()
    movie_content = scrapy.Field()

    # 按照批量数据入库方法
    schedul_item = scrapy.Field()
