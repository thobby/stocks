#!/usr/bin/env python3.3

import csv
import logging
import re
import requests
import sqlite3
import sys
import ystockquote

logging.basicConfig(level = logging.DEBUG)
logger = logging.getLogger("stocks")

class ose:
    id = 1
    name = 'ose'
    root_url = 'http://www.oslobors.no'
    stocks_list_url = root_url + '/ob_eng/markedsaktivitet/stockList?newt__list=OB-OSE'
    ticker_url = root_url + '/ob_eng/markedsaktivitet/stockOverview?newt__ticker='
    daily_values = root_url + '/markedsaktivitet/servlets/newt/tradesExcel-stock?exch=ose&newt_page=%2Fno%2Fportal%2Fose%2FstockGraph'

    def get_tickers(self):
        r = requests.get(self.stocks_list_url)
        assert(r.status_code == 200)
        tickers = [
            m.group(1) + ".OL" for m in re.finditer(re.escape(self.ticker_url) + "(\w*)", r.text)]
        tickers = set(tickers)
        return tickers

class nasdaq:
    id = 2
    name = 'nasdaq'
    filename = 'nasdaq.csv'

    def get_tickers(self):
        tickers = []
        with open(self.filename, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                tickers.append(row[0])
        tickers = set(tickers)
        return tickers

class ticker:
    id = -1
    name = ''
    def __init__(self, id, name):
        self.id = id
        self.name = name

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

    def update_tickers(self, exchange, tickers):
        for ticker in tickers:
            self.cur.execute('select t.id, t.name from tickers t, exchanges e where t.exchange = e.id and t.name = ? and e.name = ?',
                             (ticker, exchange.name,))
            row = self.cur.fetchone()
            if row is None:
                logger.info("New ticker on %s[%s]: %s", exchange.name, exchange.id, ticker)
                self.conn.execute('insert into tickers(id, exchange, name) values (null, ?, ?);', (exchange.id, ticker))
            else:
                logger.debug("Ticker %s is already in the db", ticker)

    def get_tickers(self, exchange):
        self.cur.execute('select t.id, t.name from tickers t, exchanges e where e.id = ? and e.id = t.exchange',
                    (exchange.id,))
        tickets = []
        for r in self.cur.fetchall():
            tickets.append(ticker(r[0], r[1]))
        return tickets

    def update_data_ticker(self, exchange, ticker, data):
        for d in data:
            self.cur.execute('insert into data(ticker, datum, open, close, high, low, volume, adj_close) values (?, date(?), ?, ?, ?, ?, ?, ?)',
                        (ticker.id,
                         d,
                         float(data[d]['Open']),
                         float(data[d]['Close']),
                         float(data[d]['High']),
                         float(data[d]['Low']),
                         int(data[d]['Volume']),
                         float(data[d]['Adj Close'])
                         ))


db = db()
db.open_connection()

ose = ose()
tickers = ose.get_tickers()
db.update_tickers(ose, tickers)

for t in db.get_tickers(ose):
    logger.info("Updating %s", t.name)
    try:
        data = ystockquote.get_historical_prices(t.name, "2007-01-01", "2015-01-01")
    except:
        logger.warning("Getting %s from Yahoo failed %s", t.name, sys.exc_info()[0])
    db.update_data_ticker(ose, t, data)

nasdaq = nasdaq()
tickers = nasdaq.get_tickers()
db.update_tickers(nasdaq, tickers)

for t in db.get_tickers(nasdaq):
    logger.info("Updating %s", t.name)
    try:
        data = ystockquote.get_historical_prices(t.name, "2007-01-01", "2015-01-01")
    except:
        logger.warning("Getting %s from Yahoo failed %s", t.name, sys.exc_info()[0])
    db.update_data_ticker(nasdaq, t, data)

db.close_connection()

