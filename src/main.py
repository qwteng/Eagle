# coding=utf-8

from parser.parser import *
import sys
import time

reload(sys)
sys.setdefaultencoding('utf-8')


def get_stocklist(filename):
	url_stocklist = 'http://quote.eastmoney.com/stocklist.html'
	dt = DataSource()
	list_parser = SockListParser()
	content = dt.crawl(url_stocklist)
	stock_list = list_parser.parse(content)
	
	f = open(filename,'w')
	for stock in stock_list:
		f.write(str(stock)+"\n")
	
	f.close()
	
def get_stockdata(stocklist, stockdata):
	f_list = open(stocklist, 'r')
	stock_list = f_list.readlines()
	stock = Stock()
	f_list.close()
	print(len(stock_list))

	f  = open(stockdata, 'w')

	for stockstr in stock_list:
		print(stockstr)
		s = eval(stockstr)
		code = s['code']
		print code
		
		if code[0] not in '036':
			continue
		print code    
		try:
			stock_data = stock.parse(code)
			#stock_data.update(s)
			print(type(stock_data))
			for i in stock_data.keys() :
				print(i)
			f.write(str(stock_data) + "\n")
		except:
			continue

	f.close()

if __name__ == "__main__":
	timestr = time.strftime("%Y%m%d%H%M%S", time.localtime())
	filename = "data/stock-" + timestr + ".txt"
	#get_stocklist(filename)
	get_stockdata("data/stocklist-20160313191411.txt", filename)