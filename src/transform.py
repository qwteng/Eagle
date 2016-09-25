# coding=utf-8

import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def holders2stock(file_in, file_out):
    fin = open(file_in)
    fout = open(file_out, 'w')
    stocks = {}
    for line in fin:
        json_str = unicode(line, 'UTF-8')
        holder = json.loads(json_str)
        h = holder['holder']
        name = h['holdername']
        code = holder['code']
        holders = []
        if stocks.has_key(code):
            holders = stocks[code]
        holders.append(holder['holder'])
        stocks[code] = holders
    
    for key in stocks.keys():
        stock = stocks[key]
        rels = get_holderrel(stock)
        for rel in rels:
            src = rel[0]['holdername']
            target = rel[1]['holdername']

            if len(src) > 4 or len(target) >4 :
                continue
            fout.write(src + ',' +target + ','+ "undirected" +"\n" )

def get_holder_relation(pos, holders):
    rslt = []
    if holders is None:
        return []
    holder_num = len(holders)
    if pos > holder_num -2:
        return []
    for i in range(pos+1, holder_num):
        rslt.append([holders[pos],holders[i]])
    return rslt

def get_holderrel(holders):
    rslt = []
    if holders is None:
        return []
    holder_num = len(holders)
    for i in range(0,holder_num-1):
        rslt.extend(get_holder_relation(i,holders))
    return rslt



if __name__ == "__main__":
    holders2stock('stockholder-20160630.txt', "rel.txt")