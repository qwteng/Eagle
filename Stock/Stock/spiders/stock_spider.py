# -*- coding: utf-8 -*-

import scrapy
from scrapy import Spider
from scrapy.selector import Selector

from Stock.items import StockItem

class StockSpider(Spider):
	name = "eastmoney"
	allowed_domains = ["eastmoney.com"]
	start_urls = [
		"http://quote.eastmoney.com/stocklist.html"
	]

	def is_shsz_stocklink(self, link):
		elems = link.split('.')
		if len(elems) != 4:
			return False
		if len(elems[2]) != 12:
			return False
		code = elems[2][-6:]

		return ("30000" in code)


	def parse(self, response):
		for  sel in response.xpath('//ul/li'):
			link = sel.xpath('a/@href').extract()
			if len(link) == 0 :
				continue
			url = link[0]
			if self.is_shsz_stocklink(url):
				yield scrapy.Request(url, callback=self.parse_stock_page)

	def parse_stock_page(self, response):
		for sel in response.xpath('//div[@class="cells"]'):
			links = sel.xpath(".//a")
			for l in links:
				name = l.xpath('text()').extract()
				if name[0] == u'股东研究':
					url_holders= l.xpath('@href').extract()
					yield scrapy.Request(url_holders[0], callback=self.parse_shareholderresearh)

	def parse_shareholderresearh(self, response):
		for sel in response.xpath('//div[@id="TTS_Table_Div"]'):
			print sel