from scrapy import Spider
from scrapy.selector import Selector

from Stock.items import StockItem

class StockSpider(Spider):
	name = "eastmoney"
	allowed_domains = ["eastmoney.com"]
	start_urls = [
		"http://quote.eastmoney.com/stocklist.html"
	]

	def parse(self, response):
		links = Selector(response).xpath('//ul/li')
		for  sel in links:
			item = StockItem()
			name = sel.xpath('a/text()').extract()
			item['link'] = name
			
			yield item

