# utilities used for AIM
import urllib
import csv
from datetime import datetime

def StockPrice(ticker):
    
    # uses Yahoo Finance's "download data" feature to get the current stock price
    
    baseurl = 'http://download.finance.yahoo.com/d/quotes.csv?s=%s&f=sl1d1t1c1ohgv&e=.csv'
    line = csv.reader(urllib.urlopen(baseurl % ticker), delimiter=",", quotechar='"').next()
    
    # line is a list of information (symbol, price, date, time, delta from open, open, high, low, volume)
    sp = {}
    sp['symbol'] = line[0]
    sp['price']  = line[1]
    sp['date']   = datetime.strptime(line[2],"%m/%d/%Y")
    sp['time']   = datetime.strptime(line[3],"%I:%M%p")
    sp['delta']  = line[4]
    sp['open']   = line[5]
    sp['high']   = line[6]
    sp['low']    = line[7]
    sp['volume'] = line[8]
    
    # convert the date to a YYYY-MM-DD format.
    #line[2] = "%s-%s-%s" % ( line[2][6:], line[2][:2], line[2][3:5] )
    #line[2] = datetime.strptime(line[2],"%m/%d/%Y")
    return sp

def HistoricalStockPrice(ticker, start, end):
    # ticker - ticker symbol
    # start -  start date
    # end   - end date
    
    baseurl = "http://ichart.finance.yahoo.com/table.csv?s=%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s&g=d&ignore=.csv"
    
    url = baseurl % (
        ticker,
        start.month,
        start.day,
        start.year,
        end.month,
        end.day,
        end.year
    )
    
    pricehistory = csv.reader(urllib.urlopen(url), delimiter=",", quotechar='"')
    
    retlist = []
    
    for line in pricehistory:
        retlist.append(line)
    
    return retlist