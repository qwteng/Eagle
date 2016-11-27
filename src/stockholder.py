# coding=utf-8

import sys
import time
from util.parser import *
from model.datamodel import *
from util import utils
import json
import tushare as ts

def get_top10holder_to_file(filename):
    output = open(filename, 'w+')
    stock_basics = ts.get_stock_basics()
    for index, row in stock_basics.iterrows():
        try:
            code = index
            name = row[0]
            print(code+",\t" + name)
            stock = StockInfo()
            top10holderList= stock.parse(code, name)
            if top10holderList is None:
                continue
            for top10holder in top10holderList:
                for holder in top10holder.holders:
                    output.write(json.dumps(holder.to_map(), ensure_ascii=False).decode('utf8') + "\n")
                output.write(json.dumps(top10holder.to_map(), ensure_ascii=False).decode('utf8')+"\n")
                top10holder.holders = []
                output.write(json.dumps(top10holder.to_map(), ensure_ascii=False).decode('utf8') + "\n")
        except Exception , e :
            continue

    output.close();

get_top10holder_to_file("b.txt")
