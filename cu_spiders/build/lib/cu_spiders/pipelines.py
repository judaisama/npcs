# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class CuSpidersPipeline(object):
    def process_item(self, item, spider):
        item.save()
        return item

# class PriceConverterPipeline():
#     exchang_rate = 10
#     def process_item(self, item, spider):
#

# from scrapy import Item
# import pymongo
# class MongoDBPipeline(object):
#     def from_crawler(cls, crawler):
#         cls.DB_URI = crawler.settings.get("MONGODB_URI", "mongodb://localhost:27017")
#         cls.db = crawler.settings.get("MONGODB_NAME", "scrapy_db")
#     def open_spider(self,spider):
#         self.client = pymongo.mongo_client(self.DB_URI)
#         self.db = self.client[self.DB_NAME]
#     def close_spider(self,spider):
#         self.client.close()
#     def process_item(self, item, spider):
#         insert_item = dict(item) if isinstance(item, Item) else item
#         table = self.db[spider.name]
#         table.insert_one(insert_item)
#         return item
