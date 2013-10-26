#!/usr/bin/env python2.7

#import datetime
import logging
from scipy import stats
import sqlite3

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
    datum = -1
    open = -1
    close = -1
    def __init__(self, datum, open, close):
        self.datum = datum
        self.open = open
        self.close = close

# tables:
#  exchanges: id, name
#  tickers: id, exchange, name
class db:
    file = 'stocks.db'

    def open_connection(self):
        logger.debug("Opening connection to DB %s", self.file)
        self.conn = sqlite3.connect(self.file)
        self.cur = self.conn.cursor()

    def close_connection(self):
        logger.debug("Closing connection to DB %s", self.file)
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
        self.cur.execute('select datum, open, close from data where ticker = ?',
                         (ticker.id,))
        datas = []
        for r in self.cur.fetchall():
            datas.append(data(r[0], r[1], r[2]))
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
    logger.info("Calculating linear regression %s", t.name)
    datas = db.get_ticker_data(t)
    x = []
    y = []
    i = 0
    for d in datas:
        x.append(i)
        y.append(d.close)
        i += 1
    gradient, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    print("Gradient %s Intercept %s R_value %s P_value %s Err %s" %
          (gradient, intercept, r_value, p_value, std_err))
    lrs.append(lr(t, gradient, intercept, r_value, p_value, std_err))

lrs.sort(key=lambda x: x.p_value, reverse=True)

for lr in lrs:
    print("%s %s %s" % (lr.ticker.name, lr.gradient, lr.p_value))
    db.cur.execute("insert into linear_regression(ticker, gradient, intercept, r_value, p_value, std_err) " +
               "values (?, ?, ?, ?, ?, ?)",
                (lr.ticker.id, lr.gradient, lr.intercept, lr.r_value, lr.p_value, lr.std_err));

db.close_connection()
