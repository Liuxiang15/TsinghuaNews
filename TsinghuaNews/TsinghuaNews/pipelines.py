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

    def process_item(self, item, spider):
        valid = True
        for single_new in item:
            if not single_new:  #异常处理
                valid = False
                raise DropItem("Missing {0}!".format(single_new))
            if valid:
                self.post.insert(dict(item))

        return item
