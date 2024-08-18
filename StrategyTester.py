import pandas as pd
import numpy as np
import matplotlib.style
import matplotlib.pyplot as plt
import yfinance as yf

class StrategyTester():
    def __init__(self, symbol, sma_short, sma_long, start, end):
        self.end = end
        self.start = start
        self.sma_long = sma_long
        self.sma_short = sma_short
        self.symbol = symbol
        self.results = None
        self.data = self.get_data()

    def get_data(self):
        df = yf.download(self.symbol, self.start, self.end).Close
        df.rename(columns={"Close": "price"}, inplace=True)
        return df


