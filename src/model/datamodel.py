# coding=utf-8
__author__ = 'qwteng'

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

class StockTag:
    def __init_(self):
        self.code = ""
        self.name = ""
        self.tags = []
    def to_map(self):
        map = {}
        map['code'] = self.code
        map['name'] = self.name
        map['tags'] = self.tags
        return map

class StockHolder:
    def __init__(self):
        self.code=""
        self.name=""
        self.date=""
        self.holdername=""
        self.number=""
        self.rate=""
        self.change=""
    def to_map(self):
        map = {}
        map['code'] = self.code
        map['name'] = self.name
        map['date'] = self.date
        map['holdername'] = self.holdername
        map['number'] = self.number
        map['rate'] = self.rate
        map['change'] =self.change
        return map

class StockTop10Holders:
    def __init__(self):
        self.code=""
        self.name=""
        self.date=""
        self.top10rate=""
        self.top10desc=""
        self.holders=[]
    def to_map(self):
        map = {}
        map['code'] = self.code
        map['name'] = self.name
        map['date'] = self.date
        map['top10rate'] = self.top10rate
        map['top10desc'] = self.top10desc
        l = []
        for h in self.holders:
            l.append(h.to_map())
        map['holders'] = l
        return map

        
    