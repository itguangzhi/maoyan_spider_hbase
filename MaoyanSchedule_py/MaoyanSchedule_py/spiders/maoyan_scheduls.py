# -*- coding: utf-8 -*-
import scrapy


class MaoyanSchedulsSpider(scrapy.Spider):
    name = 'maoyan_scheduls'
    allowed_domains = ['m.maoyan.com/ajax/cinemaDetail?cinemaId=154']
    start_urls = ['http://m.maoyan.com/ajax/cinemaDetail?cinemaId=154/']

    def parse(self, response):
        pass
