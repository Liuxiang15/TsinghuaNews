# -*- coding: utf-8 -*-
import scrapy
from TsinghuaNews.items import TsinghuanewsItem
from scrapy.selector import Selector


class ThunewsspiderSpider(scrapy.Spider):
    #爬虫名不能和项目名重复
    name = 'THUNewsSpider'
    allowed_domains = ['http://news.tsinghua.edu.cn']
    start_urls = ['http://news.tsinghua.edu.cn/publish/thunews/9648/2018/20181228102234212361194/20181228102234212361194_.html']

    def parse(self, response):
        #print(response.text)
        news_item = TsinghuanewsItem()
        news_item["title"] = response.selector.xpath("//title/text()").extract_first()
        news_item["keywords"] = response.selector.xpath('//meta[@name="keywords"]/@content').extract_first().split(' ')[0]
        datestr_list = response.selector.xpath('//div[@class="articletime"]/text()').extract_first().split(' ')
        day = datestr_list[0]
        time = datestr_list[1].split("\u3000")[0]
        news_item["date"] = day + time
        #单纯的以p标签作为识别
        paragraph_list = response.selector.xpath('//article[@class="article"][1]/p/text()').extract()
        content = ""
        for index, paragraph in enumerate(paragraph_list):
            print(str(index)+paragraph)
            #strong_str = Selector(text=paragraph).xpath('//strong/text()').extract()
            #print("strong_str:"+strong_str[1])
            if(paragraph == " "):
                continue
            paragraph = "".join(paragraph.split())      #split方法中不带参数时，表示分割所有换行符、制表符、空格
            paragraph = paragraph.replace("\ue863", "")#去除乱码
            content += paragraph
            content += "\n"                         #加换行符
        news_item["content"] = content
        print(news_item)
        yield news_item

    def find_tag(self):
    #本函数是为了找p段落中的strong，div等标签对应的文本，并且将他们和p标签对应文本的顺序也应该知道
    #然后顺序组装成相应段落文本
        pass
