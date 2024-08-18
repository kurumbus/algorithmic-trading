import pandas as pd
import numpy as np
import matplotlib.style
import matplotlib.pyplot as plt
import yfinance as yf


class StrategyTester():
    def __init__(self, symbol, sma_short, sma_long, start, end, rawdata):
        self.end = end
        self.start = start
        self.sma_long = sma_long
        self.sma_short = sma_short
        self.symbol = symbol
        self.rawdata = rawdata
        self.data = None  ##
        self.results = None
        self.perf = None
        self.outperf = None

    def run(self):
        self.data = self.get_data()
        self.results = self.get_results()
        self.perf = self.results['cstrategy'].iloc[-1]
        self.outperf = self.perf - self.results['creturns'].iloc[-1]

    def get_data(self):
        df = self.rawdata
        df['returns'] = np.log(df['price'] / df['price'].shift(1))
        df['sma_short'] = df['price'].rolling(self.sma_short).mean()
        df['sma_long'] = df['price'].rolling(self.sma_long).mean()
        return df

    def get_results(self):
        data = self.data.copy().dropna()
        data['position'] = np.where(data['sma_short'] > data['sma_long'], 1, -1)
        data['strategy'] = data['position'].shift(1) * data['returns']
        data.dropna(inplace=True)
        data['creturns'] = data['returns'].cumsum().apply(np.exp)
        data['cstrategy'] = data['strategy'].cumsum().apply(np.exp)
        return data

    def plot_results(self):
        title = "{} | SMA short = {} | SMA long = {}".format(self.symbol, self.sma_short, self.sma_long)
        self.results[['creturns', 'cstrategy']].plot(title=title, figsize=(20, 10))

