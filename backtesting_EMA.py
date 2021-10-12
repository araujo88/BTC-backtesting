from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from binance.client import Client
from binance.enums import *
import config
import pandas as pd
import talib as ta
from datetime import datetime, timedelta, date

client = Client(config.API_KEY, config.API_SECRET)
            
def print_file(pair, interval, name, initial_date, final_date):

    # request historical candle (or klines) data
    bars = client.get_historical_klines(pair, interval, initial_date, final_date)
    
    # delete unwanted data - just keep date, open, high, low, close
    for line in bars:
        del line[6:]
    
    # save as CSV file 
    df = pd.DataFrame(bars, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    #df.set_index('Date', inplace=True)
    df['Date'] = pd.to_datetime(df['Date'], unit='ms', origin='unix')
    df.to_csv(name)   

class double_EMA(Strategy):
    n1 = 5
    n2 = 8
    def init(self):
        self.ema1 = self.I(ta.EMA, self.data.Close, self.n1)
        self.ema2 = self.I(ta.EMA, self.data.Close, self.n2)

    def next(self):
        if crossover(self.ema1, self.ema2):
            self.buy()
        elif crossover(self.ema2, self.ema1):
            self.sell()       

dateTimeObj1 = datetime.now()
today = dateTimeObj1.strftime("%d %b, %Y")
dateTimeObj2 = date.today() - timedelta(days=365)
initial_day = dateTimeObj2.strftime("%d %b, %Y")

# Print file
filename = "BTC_1h.csv"
# print_file('BTCUSDT', '1h', filename, initial_day, today)

# Read file
prices = pd.read_csv(filename, index_col='Date', parse_dates=True)

# Backtest
backtest = Backtest(prices, double_EMA,
              cash=100000, commission=.001,
              exclusive_orders=True)
output = backtest.run()
print(filename)
print(output)
backtest.plot()

# Optimization - maximization of equity
stats, heatmap = backtest.optimize(
    n1=range(3, 20, 1),
    n2=range(3, 20, 1),
    constraint=lambda p: p.n1 < p.n2,
    maximize='Equity Final [$]',
    max_tries=200,
    random_state=0,
    return_heatmap=True)
opt_values = heatmap.sort_values().iloc[-1:]
new_ns = opt_values.index.values
double_EMA.n1 = new_ns.item(0)[0]
double_EMA.n2 = new_ns.item(0)[1]

# Backtest again with optimization
backtest = Backtest(prices, double_EMA,
              cash=100000, commission=.001,
              exclusive_orders=True)
output = backtest.run()
print(filename)
print(output)
backtest.plot()
