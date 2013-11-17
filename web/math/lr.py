#!/usr/bin/env python2.7

#import datetime
import logging
import math
from scipy import stats
import sqlite3
import json

logging.basicConfig(level = logging.DEBUG)
logger = logging.getLogger("stocks")

class ose:
    id = 1
    name = 'ose'

class nasdaq:
    id = 2
    name = 'nasdaq'

class ticker:
    id = -1
    name = ''
    def __init__(self, id, name):
        self.id = id
        self.name = name

class data:
    ticker = -1
    datum = -1
    open = -1
    close = -1
    def __init__(self, ticker, datum, open, close):
        self.ticker = ticker
        self.datum = datum
        self.open = open
        self.close = close

# tables:
#  exchanges: id, name
#  tickers: id, exchange, name
class db:
    file = 'stocks.db'

    def open_connection(self):
        #logger.debug("Opening connection to DB %s", self.file)
        self.conn = sqlite3.connect(self.file)
        self.cur = self.conn.cursor()

    def close_connection(self):
        #logger.debug("Closing connection to DB %s", self.file)
        self.conn.commit()
        self.conn.close()

    def get_tickers(self, exchange):
        self.cur.execute('select t.id, t.name from tickers t, exchanges e where e.id = ? and e.id = t.exchange',
                    (exchange.id,))
        tickets = []
        for r in self.cur.fetchall():
            tickets.append(ticker(r[0], r[1]))
        return tickets

    def get_ticker_data(self, ticker):
        self.cur.execute('select ticker, datum, open, close from data where ticker = ?',
                         (ticker.id,))
        datas = []
        for r in self.cur.fetchall():
            datas.append(data(r[0], r[1], r[2], r[3]))
        return datas

exch = nasdaq()
db = db()
db.open_connection()

class lr:
    ticker = -1
    gradient = -1
    intercept = -1
    r_value = -1
    p_value = -1
    std_err = -1
    def __init__(self, ticker, gradient, intercept, r_value, p_value, std_err):
        self.ticker = ticker
        self.gradient = gradient
        self.intercept = intercept
        self.r_value = r_value
        self.p_value = p_value
        self.std_err = std_err

lrs = []
for t in db.get_tickers(exch):
    #logger.info("Calculating linear regression %s", t.name)
    datas = db.get_ticker_data(t)
    x = []
    y = []
    i = 0
    for d in datas:
        x.append(i)
        y.append(d.close)
        i += 1
    if len(x) <= 1:
      continue
    gradient, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    lrs.append({ "t" : t.name, "g": round(gradient, 3), "i": round(intercept,
      3), "r" : round(r_value, 3) })

db.close_connection()

print(json.dumps(lrs, separators=(',',':')));

