# -*- coding: utf-8 -*-
import scrapy
from TsinghuaNews.items import TsinghuanewsItem


class ThunewsspiderSpider(scrapy.Spider):
    #爬虫名不能和项目名重复
    name = 'THUNewsSpider'
    allowed_domains = ['http://news.tsinghua.edu.cn']
    start_urls = ['http://news.tsinghua.edu.cn/publish/thunews/9648/2018/20181228102234212361194/20181228102234212361194_.html']

    def parse(self, response):
        #print(response.text)
        news_item = TsinghuanewsItem()
        news_item["title"] = response.xpath("//title/text()").extract_first()
        news_item["keywords"] = response.xpath('//meta[@name="keywords"]/@content').extract_first().split(' ')[0]
        datestr_list = response.xpath('//div[@class="articletime"]/text()').extract_first().split(' ')
        day = datestr_list[0]
        time = datestr_list[1].split("\u3000")[0]
        news_item["date"] = day + time
        #单纯的以p标签作为识别
        paragraph_list = response.xpath('//article[@class="article"][1]/p/text()').extract()
        content = ""
        for index, paragraph in enumerate(paragraph_list):
            print(str(index)+paragraph)
            content += paragraph
        news_item["content"] = content
        print(news_item)
        yield news_item
