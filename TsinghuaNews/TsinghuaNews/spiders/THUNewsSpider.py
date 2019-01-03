# -*- coding: utf-8 -*-
import scrapy
from TsinghuaNews.items import TsinghuanewsItem
from scrapy.selector import Selector
from scrapy.exceptions import DropItem

import html2text
h = html2text.HTML2Text()
h.ignore_links = False
h.ignore_images = True


class ThunewsspiderSpider(scrapy.Spider):
    #爬虫名不能和项目名重复
    name = 'THUNewsSpider'
    allowed_domains = ['news.tsinghua.edu.cn']
    count = 0
    
    #中文新闻网1245栏目大约18000个网页
    def start_requests(self):
        # url_list = [9648, 10303, 9650, 9652]
        # page_num_list = [39, 479, 329, 16]
        url_list = [9655]
        # page_num_list = [32]
        page_num_list = [3]
        for index, i in enumerate(url_list):
            for j in range(2, page_num_list[index] + 1):
                yield scrapy.Request(
                    url =  'http://news.tsinghua.edu.cn/publish/thunews/{}/index_{}.html'.format(i, j),
                    callback = self.get_urls
                )

    def get_urls(self, response):
        # print("----------------------------------")
        #此处的xPath路径是对专题新闻的摘取
        url_list = response.selector.xpath('//section[@class="colunm1"]/ul/li/div/h3/a/@href').extract()
        domain_name = 'http://news.tsinghua.edu.cn'
        for index, path in enumerate(url_list):
            print("专题一级url是"+domain_name+path)
        max_spe_num = 10    #默认每个专题下最多的页数是10
        # for path in enumerate(url_list):
        #     print(domain_name+path)
        #     yield scrapy.Request(
        #         url=domain_name+path,
        #         callback= self.get_speurls
        #     )
        for index, path in enumerate(url_list):
            for i in range(2, max_spe_num):
                str_index = str("_{}.html".format(i))
                new_url = domain_name + url_list[index]
                new_url = new_url[:-5] + str_index
                print("新的url是"+new_url)
                yield scrapy.Request(
                    url=new_url,
                    callback=self.get_speurls
                )

    #//ul[@class="timenewslist withtopborder"]/li/div/h3/a/@href
    
    def get_speurls(self, response):
        speurl_list = response.selector.xpath('//ul[@class="timenewslist withtopborder"]/li/div/h3/a/@href').extract()
        domain_name = 'http://news.tsinghua.edu.cn'
        for index, path in enumerate(speurl_list):
            yield scrapy.Request(
                url=domain_name+path,
                callback=lambda response, url=domain_name+path:self.parse(response, url)
            )
    
    def parse(self, response, url):
        #print(response.text)
        news_item = TsinghuanewsItem()
        news_item["url"] = url
        # try:
        news_item["title"] = response.selector.xpath("//title/text()").extract_first()
        news_item["keywords"]  = response.selector.xpath('//meta[@name="keywords"]').extract_first().split(' ')[0]
        # print("关键词是：")
        # print(response.selector.xpath('//meta[@name="keywords"]/@content').extract())
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
            if (paragraph == ""):
                continue
            content += paragraph
            content += "\n"                              # 加换行符
        news_item["content"] = content
        if news_item["content"] == "" or news_item["date"] == "" or news_item["keywords"] == "":
            raise DropItem("提取正文、日期、关键词出错")
        self.count += 1
        print("成功解析的中文网页数量为：" + str(self.count))
        # print(news_item)
        yield news_item
        # except:
        #     raise DropItem("解析专题网页出错")
            

