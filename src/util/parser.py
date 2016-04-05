# coding=utf-8
__author__ = 'qwteng'

import urllib2
from bs4 import BeautifulSoup
import re
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
class DataSource:
    def crawl(self, url):
         headers = {
             'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
         }

         req = urllib2.Request(url, headers=headers)
         content = urllib2.urlopen(req).read()
         
         self.content = BeautifulSoup(content, 'lxml', from_encoding="utf-8")
        
         return self.content
        
		 
class Parser:
    def parse(self, content):
        return None

class SockListParser(Parser):
    def __init__(self):
        self.list = []
    def parse(self, content):
        stock_list = content.find_all('a', target="_blank")
        pattern = re.compile(r'.*\d{6}.', re.UNICODE)
        for stock in stock_list:
            stock_string = stock.string
            if stock_string and pattern.match(stock_string):
                stock_map = {}
                code = stock_string[-7:-1]
                name = stock_string[0:-8]
                #href = stock['href']
                stock_map['code']  = code
                stock_map['name'] = name
                self.list.append(stock_map)

        return self.list

class StockF10ReqParser(Parser):
    def __init__(self):
        self.data = {}
        self.data['earnings'] = ''
        self.data['net'] = ''
        self.data['cash'] = ''
        
    def parse(self, content):
        tables = content.find_all('table')

        for table in tables:
            spans = table.find_all('span')

            if spans:

                for i in range(len(spans)):
                    tag = spans[i].string
                    if tag == u'基本每股收益(元)':
                        self.data['earnings'] = spans[i+1].string
                    if tag == u'每股净资产(元)':
                        self.data['net'] = spans[i+1].string
                    if tag == u'每股经营现金流(元)':
                        self.data['cash'] = spans[i+1].string
        return self.data

class StockF10HolderParser(Parser):
    def __init__(self):
        self.data = {}
    def parse(self, content):
        divs = content.find_all('div', "section")
        holders_map = {}
        holders = []
        for div in divs:
            div_name = div.find('div', 'name')
           
            if div_name.strong.string != u'十大流通股东':
                continue

            holder_type = div_name.strong.string
            div_content = div.find('div', 'content')
            
            if div_content is None:
                continue

            div_tab = div_content.find('div', 'tab')
          
            if div_tab is None:
                continue

            span_dates = div_tab.find_all('span')
          
            dates = []
            for span in span_dates:
                dates.append(span.string)

            div_tables = div_content.find('div', 'content')
            if div_tables is None:
                continue

            tables = div_tables.find_all('table')
            for i in range(0, len(dates)):
                table = tables[i]
                date = dates[i]
                trs = table.find_all('tr')

                for tr in trs:
                    holder = {}
                    tds = tr.find_all('td')
                    if len(tds) < 6:
                        continue
                    name = tds[0].string
                    account = tds[3].string
                    rate = tds[4].string
                    change = tds[5].string
                    holder['name'] = name
                    holder['account'] = account
                    holder['rate'] = rate
                    holder['change'] = change
                    holder['date'] = date
                    holders.append(holder)


        if holders is not None:
            holders_map[holder_type] = holders

        return holders_map

class Stock:
    OperationsRequired_url = 'http://f10.eastmoney.com/f10_v2/OperationsRequired.aspx?code='
    ShareholderResearch_url = 'http://f10.eastmoney.com/f10_v2/ShareholderResearch.aspx?code='
    def __init__(self):
        self.datasource = DataSource()
        self.or_parser = StockF10ReqParser()
        self.sr_parser = StockF10HolderParser()
    def parse(self,code):
        stock = {}
        if code is None or len(code) != 6:
            return stock

        if code[0] == '6':
            or_url = Stock.OperationsRequired_url + 'sh' + code
            sr_url = Stock.ShareholderResearch_url + 'sh' + code
        else:
            or_url = Stock.OperationsRequired_url + 'sz' + code
            sr_url = Stock.ShareholderResearch_url + 'sz' + code

        stock['code'] = code
        or_content = self.datasource.crawl(or_url)
        stock.update(self.or_parser.parse(or_content))

        sr_content = self.datasource.crawl(sr_url)
        stock.update(self.sr_parser.parse(sr_content))

        return stock