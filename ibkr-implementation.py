import datetime

from ib_insync import *
import pandas as pd
import numpy as np
import datetime as dt
import os

ib = IB()
ib.connect()

sma_s = 2
sma_l = 5
freq = '1 min'
units = 1000
end_time = dt.time(3,55, 0)
contract = Forex("EURUSD")
ib.qualifyContracts(contract)
cfd = CFD('EUR', currency='USD')
ib.qualifyContracts(cfd)
conID = cfd.conId





def on_bar_update(bars, hasNewBar):
    global df, last_bar_date, df_strategy

    if bars[-1].date > last_bar_date:
        last_bar_date = bars[-1].date

        #data processing
        df = pd.DataFrame(bars)[['date', 'open', 'high', 'low', 'close']].iloc[:-1]
        df.set_index('date', inplace=True)

        ##### TRADING STRATEGY
        df_strategy = df[['close']].copy()
        df_strategy['sma_s'] = df_strategy.close.rolling(sma_s).mean()
        df_strategy['sma_l'] = df_strategy.close.rolling(sma_l).mean()
        df_strategy.dropna(inplace=True)
        df_strategy['position'] = np.where(df_strategy['sma_s'] > df_strategy['sma_l'], 1, -1)
        ######################

        #target = df_strategy['position'][-1] * units

        target = df_strategy['position'].iloc[-1] * units
        execute_trade(target = target)

        os.system('cls')
    #    print(df)
    else:
        try:
            trade_reporting()
        except Exception as error:
            print("An exception occurred:", error)
            pass

def execute_trade(target):
    global current_pos

    try:
        current_pos = [pos.position for pos in ib.positions() if pos.contract.conId == conID][0]
    except:
        current_pos = 0

    trades = target - current_pos


    if trades > 0:
        side = "BUY"
        order = MarketOrder(side, abs(trades))
        trade = ib.placeOrder(cfd, order)
    elif trades < 0:
        side = "SELL"
        order = MarketOrder(side, abs(trades))
        trade = ib.placeOrder(cfd, order)
    else:
        pass

def trade_reporting():
    global report
    fill_df = util.df([fs.execution for fs in ib.fills()])[['execId', 'time', 'side', 'cumQty', 'avgPrice']].set_index('execId')
    profit_df = util.df([fs.commissionReport for fs in ib.fills()])[['execId', 'realizedPNL']].set_index('execId')

    report = pd.concat([fill_df, profit_df], axis=1).set_index('time').loc[session_start:]
    report = report.groupby('time').agg({'side':'first', 'cumQty':'max', 'avgPrice':'mean', 'realizedPNL': 'sum'})
    report['cumPNL'] = report.realizedPNL.cumsum()

    os.system('cls')
    print(report)

if __name__ == '__main__':

    session_start = pd.to_datetime(dt.datetime.now(datetime.UTC))

    bars = ib.reqHistoricalData(
        contract,
        endDateTime='',
        durationStr='1 D',
        barSizeSetting=freq,
        whatToShow='MIDPOINT',
        useRTH=True,
        formatDate=2,
        keepUpToDate=True
    )

    last_bar_date = bars[-1].date
    bars.updateEvent += on_bar_update

    while True:
        ib.sleep(5)
        if dt.datetime.now(datetime.UTC).time() >= end_time:
            execute_trade(target= 0)
            ib.cancelHistoricalData(bars)
            ib.sleep(10)
            try:
                trade_reporting()
            except:
                pass
            print('Session Stopped')
            ib.disconnect()
            break
        else:
            pass



