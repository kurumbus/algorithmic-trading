import numpy as np
import pandas as pd
import matplotlib.style
import matplotlib.pyplot as plt
pd.options.display.float_format = '{:.6f}'.format
plt.style.use("seaborn-v0_8")


class IterativeBase():

    def __init__(self, symbol, start, end, amount, use_spread=True):
        self.end = end
        self.use_spread = use_spread
        self.symbol = symbol
        self.start = start
        self.initial_balance = amount
        self.current_balance = amount
        self.units = 0
        self.trades = 0
        self.position = 0
        self.data = self.get_data()
        self.balance_history = pd.DataFrame(columns=['Datetime', 'balance'])

    def get_data(self):
        df = pd.read_csv('eurusd_minute.csv', usecols=['Date', 'Time', 'BC', 'AC'])
        df['Datetime'] = df['Date'] + ' ' + df['Time']
        df['Datetime'] = pd.to_datetime(df['Datetime'])
        df = df.drop(['Date', 'Time'], axis=1)
        df = df.set_index('Datetime')
        df.rename(columns={"BC": "bid", "AC": "ask"}, inplace=True)
        df.bid = df.bid.ffill()
        df.ask = df.ask.ffill()
        df['price'] = (df['bid'] + df['ask']) / 2
        df['spread'] = df['ask'] - df['bid']
        df['returns'] = np.log(df['price'].div(df['price'].shift(1)))
        df = df.resample('1h').mean().ffill()
        return df

    def buy(self, bar, units=None, amount=None):
        date, bid, ask, spread = self.get_values(bar)
        if amount is not None:
            units = int(amount / ask)
        self.current_balance -= units * ask
        self.units += units
        self.trades += 1
        trading_cost = units * spread / 2
        self.balance_history.loc[len(self.balance_history)] = {'Datetime': date, 'balance': (
                    self.current_balance + self.units * ((bid + ask) / 2))}
        print("{} | Buying {} for {} | Trading Cost is {}".format(date, units, round(ask, 2), trading_cost))

    def sell(self, bar, units=None, amount=None):
        date, bid, ask, spread = self.get_values(bar)
        if amount is not None:
            units = int(amount / bid)
        self.current_balance += units * bid
        self.units -= units
        self.trades += 1
        trading_cost = np.abs(units) * spread / 2
        self.balance_history.loc[len(self.balance_history)] = {'Datetime': date, 'balance': (
                    self.current_balance + self.units * ((bid + ask) / 2))}
        print("{} | Selling {} for {} | Trading Cost is {}".format(date, units, round(bid, 2), trading_cost))

    def plot_data(self, cols=None):
        if cols == None:
            cols = 'price'
        self.data[cols].plot(figsize=(12, 8), title=self.symbol)

    def get_values(self, bar):
        date = str(self.data.index[bar])
        bid = round(self.data.bid.iloc[bar], 6)
        ask = round(self.data.ask.iloc[bar], 6)
        spread = round(self.data.spread.iloc[bar], 6)
        return date, bid, ask, spread

    def print_current_balance(self, bar):
        date, bid, ask, spread = self.get_values(bar)
        print("{} | Current Balance: {}".format(date, round(self.current_balance, 2)))

    def print_current_position(self, bar):
        date, bid, ask, spread = self.get_values(bar)
        price = (bid + ask) / 2
        cpv = self.units * price
        print("{} | Current Position Value: {}".format(date, round(cpv, 2)))

    def print_current_nav(self, bar):
        date, bid, ask, spread = self.get_values(bar)
        price = (bid + ask) / 2
        nav = self.current_balance + self.units * price
        print("{} | Current Nav: {}".format(date, round(nav, 2)))

    def close_pos(self, bar):
        date, bid, ask, spread = self.get_values(bar)
        price = ask if self.units < 0 else bid
        trading_cost = np.abs(self.units) * spread / 2
        print(75 * '-')
        print("{} | Closing Position of {} for {} | Trading Cost is {} ".format(date, self.units, price, trading_cost))
        print(75 * '-')
        self.current_balance += self.units * price
        self.units = 0
        self.trades += 1
        perf = (self.current_balance - self.initial_balance) / self.initial_balance * 100
        self.print_current_balance(bar)
        print("{} | Net Performance (%) = {}".format(date, round(perf, 2)))
        print("{} | Number of trades executed = {}".format(date, self.trades))
        print(75 * '-')