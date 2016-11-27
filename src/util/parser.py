# coding=utf-8
__author__ = 'qwteng'

import urllib2
from bs4 import BeautifulSoup
from model.datamodel import *
import re
import arrow
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
    def pasre_holders_sum(self, table):
        top10holderlist = []
        dateList = []
        descList = []
        rateList = []
        if table is None:
            return None
        trs = table.find_all('tr')
        for tr in trs:
            th0 = tr.find('th')
            if th0.string is None:
                ths = tr.find_all('th', attrs={"class": "tips-dataL"})
                for th in ths:
                    dateList.append(arrow.get(th.string,'YY-MM-DD').format('YYYY-MM-DD'))
            if th0.string == u'筹码集中度' :
                tds = tr.find_all('td',  attrs={"class": "tips-dataL"})
                for td in tds:
                    descList.append(td.string)
            if th0.string == unicode('前十大流通股东持股合计(%)'):
                tds = tr.find_all('td', attrs={"class": "tips-dataL"})
                for td in tds:
                    rateList.append(td.string)
        for i in range(0, len(dateList)):
            s = StockTop10Holders()
            s.date = dateList[i]
            s.top10desc = descList[i]
            s.top10rate = rateList[i]
            top10holderlist.append(s)
        return top10holderlist


    def parse_holders(self, divs):
        holderList = []
        if divs is None:
            return None
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
                    number = tds[3].string
                    rate = tds[4].string
                    change = tds[5].string
                    h = StockHolder()
                    h.date = date
                    h.holdername = name
                    h.number = number
                    h.rate = rate
                    holderList.append(h)
        return holderList

    def parse(self, content):
        div_top10 = content.find(id="Table0")
        if div_top10 is None:
            return None
        top10holderList = self.pasre_holders_sum(div_top10)

        divs = content.find_all('div', "section")
        if divs is None:
            return None
        holders = self.parse_holders(divs)

        if top10holderList is None:
            return None
        if holders is None:
            return None
        for top10holder in top10holderList:
            date = top10holder.date
            for holder in holders:
                if holder.date == date :
                    top10holder.holders.append(holder)

        return top10holderList

class StockInfo:
    OperationsRequired_url = 'http://f10.eastmoney.com/f10_v2/OperationsRequired.aspx?code='
    ShareholderResearch_url = 'http://f10.eastmoney.com/f10_v2/ShareholderResearch.aspx?code='
    def __init__(self):
        self.datasource = DataSource()
        self.or_parser = StockF10ReqParser()
        self.sr_parser = StockF10HolderParser()

    def parse(self,code,name):
        stock = {}
        if code is None or len(code) != 6:
            return stock

        if code[0] == '6':
            or_url = StockInfo.OperationsRequired_url + 'sh' + code
            sr_url = StockInfo.ShareholderResearch_url + 'sh' + code
        else:
            or_url = StockInfo.OperationsRequired_url + 'sz' + code
            sr_url = StockInfo.ShareholderResearch_url + 'sz' + code

        stock['code'] = code
        or_content = self.datasource.crawl(or_url)
        stock.update(self.or_parser.parse(or_content))

        sr_content = self.datasource.crawl(sr_url)
        top10holderList = self.sr_parser.parse(sr_content)
        if top10holderList is None:
            return None
        for top10holder in top10holderList:
            top10holder.code = code
            top10holder.name = name
            for holder in top10holder.holders:
                holder.code = code
                holder.name = name

        return top10holderList