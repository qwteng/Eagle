# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from scrapy.conf import settings
#from scrapy import log

class StockPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoDBPipeline(object):
	def __init__(self, mongodb_server, mongodb_port, mongodb_db, mongodb_collection):
		self.mongodb_server = mongodb_server
		self.mongodb_port = mongodb_port
		self.mongodb_db = mongodb_db
		self.mongodb_collection = mongodb_collection
	
	@classmethod
	def from_crawler(cls, crawler):
		print "in crawler"
		return cls(
			mongodb_server= crawler.settings.get('MONGODB_SERVER'),
			mongodb_port =  int(crawler.settings.get('MONGODB_PORT')),
			mongodb_db=crawler.settings.get('MONGODB_DB'),
			mongodb_collection=crawler.settings.get('MONGODB_COLLECTION')
		)

	def open_spider(self, spider):
		self.client = MongoClient(self.mongodb_server, self.mongodb_port)
		self.db = self.client[self.mongodb_db]
		self.collection = self.db[self.mongodb_collection]

	def close_spider(self, spider):
		self.client.close()

	def process_item(self, item, spider):
		print "in pipeline"
		#log.msg("begin insert data", level=log.DEBUG, splider=splider)
		self.collection.insert(dict(item))
			

		return item