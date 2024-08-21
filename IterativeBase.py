class IterativeBase():

    def __init__(self, symbol, start, end, amount):
        self.symbol = symbol
        self.start = start
        self.initial_balance = amount
        self.current_balance = amount
        self.units = 0
        self.trades = 0
        self.data = self.get_data()

    def get_data(self):
        df = pd.read_csv('eurusd_minute.csv', usecols=['Date', 'Time', 'BC', 'AC'])
        df['Datetime'] = df['Date'] + ' ' + df['Time']
        df['Datetime'] = pd.to_datetime(df['Datetime'])
        df = df.drop(['Date', 'Time'], axis=1)
        df = df.set_index('Datetime')
        df.rename(columns={"BC": "bid", "AC": "ask"}, inplace=True)
        df['price'] = (df['bid'] + df['ask']) / 2
        df['spread'] = df['ask'] - df['bid']
        df['returns'] = np.log(df['price'].div(df['price'].shift(1)))
        return df

    def buy(self, bar, units=None, amount=None):
        date, price, spread = self.get_values(bar)
        if amount is not None:
            units = int(amount / price)
        self.current_balance -= units * price
        self.units += units
        self.trades += 1
        print("{} | Buying {} for {}".format(date, units, round(price, 2)))

    def plot_data(self, cols=None):
        if cols == None:
            cols = 'price'
        self.data[cols].plot(figsize=(12, 8), title=self.symbol)

    def get_values(self, bar):
        date = str(self.data.index[bar].date())
        price = round(self.data.price.iloc[bar], 6)
        spread = round(self.data.spread.iloc[bar], 6)
        return date, price, spread

    def print_current_balance(self, bar):
        date, price, spread = self.get_values(bar)
        print("{} | Current Balance: {}".format(date, round(self.current_balance, 2)))

    def print_current_position(self, bar):
        date, price, spread = self.get_values(bar)
        cpv = self.units * price
        print("{} | Current Position Value: {}".format(date, round(cpv, 2)))

    def print_current_nav(self, bar):
        date, price, spread = self.get_values(bar)
        nav = self.current_balance + self.units * price
        print("{} | Current Nav: {}".format(date, round(nav, 2)))