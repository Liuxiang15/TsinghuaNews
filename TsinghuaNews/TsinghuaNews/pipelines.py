# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from TsinghuaNews.settings import mongo_host,mongo_port,mongo_db_name,mongo_db_collection
from scrapy.exceptions import DropItem

class TsinghuanewsPipeline(object):
    def __init__(self):
        host = mongo_host
        port = mongo_port
        dbname = mongo_db_name
        sheetname = mongo_db_collection
        client = pymongo.MongoClient(host=host, port=port)
        mydb = client[dbname]
        self.post = mydb[sheetname]
        self.url_sets = set()
        self.title_sets = set()
    def process_item(self, item, spider):
        item_dict = dict(item)
        if not item_dict:   #判断是否为空
            raise DropItem("数据错误!")
        if item_dict["title"] in self.title_sets or item_dict["url"] in self.url_sets:
            raise DropItem("Duplicate item found")
        else:
            exist_flag = True
            for data in self.post.find():
                if item_dict["title"] == data["title"] or item_dict["url"] == data["url"]:
                    exist_flag = False
                    break
            if exist_flag:
                new_id = self.post.insert(item_dict)
                self.url_sets.add(item_dict["url"])
                self.title_sets.add(item_dict["title"])
            