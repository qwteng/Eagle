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
		md5 = utils.md5(str(h))
		h['md5'] = md5
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
	for st in st_list:
		if not st.has_key('code'):
			continue
		code = st['code']
		print code
		try:
			stock_info = stock.parse(code)
		except:
			continue

		c_stockinfo.update({'code':code}, {"$set":stock_info})
		try:
			holders = get_holders(stock_info)
		except:
			continue
		for h in holders:
			r = c_holders.find_one({'md5':h['md5']})
			if r is None:
				c_holders.insert(h)