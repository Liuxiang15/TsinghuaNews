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

    def process_item(self, item, spider):
        valid = True
        for data in item:
            # print("-------------single_new----------------------")
            # print(data)
            # print("-------------single_new!!----------------------")
            if not data:  #异常处理
                valid = False
                raise DropItem("Missing {0}!".format(data))
            if valid:
                item_dict = dict(item)
                if item_dict["url"] in self.url_sets:
                    print("集合中的url是")
                    print(self.url_sets)
                    raise DropItem("Duplicate item found: %s" % item)
                    
                else:
                    self.url_sets.add(item_dict["url"])
                    self.post.insert(item_dict)
                    return item
