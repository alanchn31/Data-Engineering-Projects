# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymongo

class MongoDBPipeline(object):

    def __init__(self, mongo_uri, mongo_db, collection_name):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_name = collection_name
    
    @classmethod
    def from_crawler(cls, crawler):
        # pull info from settings.py
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DB'),
            collection_name = crawler.settings.get('MONGO_COLLECTION')
        )
    
    def open_spider(self, spider):
        # initialize spider
        # open db connection
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        # clean up when spider is closed
        self.client.close()

    def process_item(self, item, spider):
        print('collection:', self.collection_name)
        self.db[self.collection_name].insert(dict(item))
        logging.debug("Title added to MongoDB")
        return item
