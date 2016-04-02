# coding=utf-8


import sys
import time
from pymongo import MongoClient
from util.parser import *

reload(sys)
sys.setdefaultencoding('utf-8')



def get_stocklist():
	url_stocklist = 'http://quote.eastmoney.com/stocklist.html'
	dt = DataSource()
	list_parser = SockListParser()
	content = dt.crawl(url_stocklist)
	stock_list = list_parser.parse(content)
	
	return stock_list
	
def get_stockdata(stockcode):
	
	if stockcode[0] not in '036':
		return None
	
	stock = Stock()

	stock_data = None
	try:
		stock_data = stock.parse(code)
	except:
		pass
	
	return stock_data

if __name__ == "__main__":
	timestr = time.strftime("%Y%m%d%H%M%S", time.localtime())
	client = MongoClient()
	stockdb = client['stock']
	collection = stockdb['stockinfo']
	
	list = get_stocklist()
	collection.insert(list)
	
	stock = Stock()

	st_list = collection.find()
	for st in st_list:
		if not st.has_key('code'):
			continue
		code = st['code']
		stock_info = stock.parse('600106')
		collection.update({'code':code}, stock_info)
