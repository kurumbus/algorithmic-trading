from IterativeBase import IterativeBase


class IterativeBacktest(IterativeBase):
    def go_long(self, bar, units=None, amount=None):
        if self.position == -1:
            self.buy(bar, units=-self.units)
        if units:
            self.buy(bar, units=units)
        elif amount:
            if amount == 'all':
                amount = self.current_balance
            self.buy(bar, amount=amount)

    def go_short(self, bar, units=None, amount=None):
        if self.position == 1:
            self.sell(bar, units=self.units)
        if units:
            self.sell(bar, units=units)
        elif amount:
            if amount == 'all':
                amount = self.current_balance
            self.sell(bar, amount=amount)

    def test_sma_strategy(self, sma_s, sma_l):
        stm = "Testing SMA | {} | {} Sma Short | {} Sma Long".format(self.symbol, sma_s, sma_l)
        print('-' * 75)
        print(stm)
        print('-' * 75)
        # reset
        self.position = 0
        self.trades = 0
        self.current_balance = self.initial_balance
        self.data = self.get_data()

        self.data['sma_short'] = self.data['price'].rolling(sma_s).mean()
        self.data['sma_long'] = self.data['price'].rolling(sma_l).mean()
        self.data.dropna(inplace=True)

        for bar in range(len(self.data) - 1):  # all bars
            if self.data['sma_short'].iloc[bar] > self.data['sma_long'].iloc[bar]:
                # print('point2 {}'.format(bar))
                if self.position in [0, -1]:
                    self.go_long(bar, amount='all')
                    self.position = 1
                    print("bar: {} | long: sma s {} > sma l {}".format(bar, self.data['sma_short'].iloc[bar],
                                                                       self.data['sma_long'].iloc[bar]))
            elif self.data['sma_short'].iloc[bar] < self.data['sma_long'].iloc[bar]:
                # print('point4 {}'.format(bar))
                if self.position in [0, 1]:
                    self.go_short(bar, amount='all')
                    self.position = -1
                    print("bar: {} | short: sma s {} < sma l {}".format(bar, self.data['sma_short'].iloc[bar],
                                                                        self.data['sma_long'].iloc[bar]))
        self.close_pos(bar + 1)  # close position at the last bar