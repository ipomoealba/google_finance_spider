#!/bin/python
# -*- encoding:utf-8 -*-
# works fine with Python 2.7.9 (not 3.4.+)
import urllib2
import json
import datetime
import sys
import os


def fetchMarketHistoryData(symbol, exchange=""):
    link = "http://www.google.com/finance/getprices?q=AAPL&i=300&p=10d&f=d,o,h,l,c,v"
    interval_time = 60
    if exchange == "":
        url = link + \
            "q=%s&i=%d&p=%s&f=d,o,h,l,c,v" % (symbol, interval_time, "10Y")
    else:
        url = link + \
            "q=%s&x=%s&i=%d&p=%s&f=d,o,h,l,c,v" % (
                symbol, exchange, interval_time, "10Y")

    raw_data = urllib2.urlopen(url)
    content = raw_data.read()
    # 7th row is starttime stamp , use linux like timestamp
    start_unix_timestamp = float(content.split("\n")[7].split(",")[0][1:])
    starttime = datetime.datetime.fromtimestamp(
        start_unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    # after 8th rows is history data
    for i in content.split("\n")[8:]:
        result = (i.split(","))
        if len(result[0]) > 5:
            start_unix_timestamp = float(result[0][1:])
        elif len(result[0]) < 5 and result[0] != "":
            now_unix_timestamp = start_unix_timestamp + \
                float(result[0]) * interval_time
            result[0] = datetime.datetime.fromtimestamp(
                now_unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')

            print(result)


if __name__ == '__main__':
    hint = """
    python spider.py --symbol stock_symbol
    python spider.py -s stock_symbol
    python spider.py --target targetfile
    python spider.py -t targetfile

    and your data will save in \"data\" file
    """
    if len(sys.argv) > 1:
        arg = sys.argv[1].replace(" ", "")
        if arg == "--symbol" or arg == "-s":
            print(arg)
            fetchMarketHistoryData(sys.argv[2])
        elif arg == "--target" or arg == "-t":
            f = open(sys.argv[2], "r")
            for line in f.readline():
                if len(line.split(" ")) > 1:
                    stock_symbol = line.split(" ")[0]
                    exchange = line.split(" ")[1]
                    t = fetchMarketHistoryData(stock_symbol, exchange=exchange)
                else:
                    stock_symbol = line.split(" ")[0]
                    fetchMarketHistoryData(stock_symbol)
        else:
            print(hint)
    else:
        print(hint)
