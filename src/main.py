# coding=utf-8


import sys
import time
from pymongo import MongoClient
from util.parser import *
from util import utils

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
		pas
	
	return stock_data

def get_holders(stockdata):
	if stockdata is None:
		return None
	rslt = []
	basic = {}
	basic['code'] = stockdata['code']
	# basic['name'] = stockdata['name']
	basic['net'] = stockdata['net']
	basic['earnings'] = stockdata['earnings']
	basic['cash'] = stockdata['cash']
	holders = stockdata[u'十大流通股东']
	for holder in holders:
		h = {}
		h.update(basic)
		h.update(holder)
		rslt.append(h)
	return rslt

if __name__ == "__main__":
	timestr = time.strftime("%Y%m%d%H%M%S", time.localtime())
	client = MongoClient()
	stockdb = client['stock']
	c_stockinfo = stockdb['stockinfo']
	c_holders = stockdb['stockholders']
	stock_list = get_stocklist()
	c_stockinfo.insert(stock_list)
	
	stock = Stock()
	st_list = c_stockinfo.find()
	print st_list
	for st in st_list:
		if not st.has_key('code'):
			continue
		code = st['code']
		stock_info = stock.parse(code)
		c_stockinfo.update({'code':code}, {"$set":stock_info})
		holders = get_holders(stock_info)
		if holders is not None and len(holders) != 0:
			c_holders.insert(holders)