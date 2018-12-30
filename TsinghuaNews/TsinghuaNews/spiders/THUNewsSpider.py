# -*- coding: utf-8 -*-
import scrapy
from TsinghuaNews.items import TsinghuanewsItem
from scrapy.selector import Selector

import html2text
h = html2text.HTML2Text()
h.ignore_links = False
h.ignore_images = True


class ThunewsspiderSpider(scrapy.Spider):
    #爬虫名不能和项目名重复
    name = 'THUNewsSpider'
    allowed_domains = ['news.tsinghua.edu.cn']
    current_url = ""



    #头条http://news.tsinghua.edu.cn/publish/thunews/9648/index.html 39
    #综合新闻http://news.tsinghua.edu.cn/publish/thunews/10303/index.html  479
    #start_urls = ['http://news.tsinghua.edu.cn/publish/thunews/9648/2018/20181228102234212361194/20181228102234212361194_.html']
    def start_requests(self):
        #测试先获取10个网址
        for i in range(2,3):
            yield scrapy.Request(
                url =  'http://news.tsinghua.edu.cn/publish/thunews/10303/index_{}.html'.format(i),
                callback = self.get_urls
            )

    def get_urls(self, response):
        # print("----------------------------------")
        url_number = 21
        url_list = response.selector.xpath('//section[1]/ul/li/figure/figcaption/a/@href').extract()
        domain_name = 'http://news.tsinghua.edu.cn'
        for index, path in enumerate(url_list):
            yield scrapy.Request(
                url=domain_name+path,
                callback=lambda response, url=domain_name+path:self.parse(response, url)
            )

    def parse(self, response, url):
        #print(response.text)
        news_item = TsinghuanewsItem()
        news_item["url"] = url
        news_item["title"] = response.selector.xpath("//title/text()").extract_first()
        news_item["keywords"] = response.selector.xpath('//meta[@name="keywords"]/@content').extract_first().split(' ')[0]
        datestr_list = response.selector.xpath('//div[@class="articletime"]/text()').extract_first().split(' ')
        day = datestr_list[0]
        time = datestr_list[1].split("\u3000")[0]
        news_item["date"] = day + time
        #单纯的以p标签作为识别
        paragraph_list = ""
        if("组图" in news_item["title"] or "图片传真" in news_item["title"]):
            paragraph_list = response.selector.xpath('//article[ @class ="article"][1]').extract()
        else:
            paragraph_list = response.selector.xpath('//article[@class="article"][1]/p').extract()

        content = ""
        for index, paragraph in enumerate(paragraph_list):
            paragraph = h.handle(paragraph)
            paragraph = paragraph.replace("\ue863", "")  # 去除乱码
            paragraph = paragraph.replace("\n", "")      #去除换行符
            content += paragraph
            content += "\n"                              # 加换行符
        # content = ""
        # for index, paragraph in enumerate(paragraph_list):
        #     print(str(index)+paragraph)
        #     #strong_str = Selector(text=paragraph).xpath('//strong/text()').extract()
        #     #print("strong_str:"+strong_str[1])
        #     if(paragraph == " "):
        #         continue
        #     paragraph = "".join(paragraph.split())      #split方法中不带参数时，表示分割所有换行符、制表符、空格
        #     paragraph = paragraph.replace("\ue863", "")#去除乱码
        #     content += paragraph
        #     content += "\n"                         #加换行符
        news_item["content"] = content
        # print(news_item)
        yield news_item


