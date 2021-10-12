# BTC-backtesting
 Bitcoin trading strategy backtesting on Python using libraries TA-Lib, Pandas, Binance API and Backtesting.
 
 On the example implemented, a simple EMA (Exponential Moving Average) crossing trading strategy is tested and its parameters (time interval of each EMA) are optimized. The data utilized was the BTC/USDT 1h candle closing price (1 year interval). The backtesting starts with intervals of 5 periods and 8 periods for the low and fast EMA respectively and, after optimization, 17 and 19 for each one.
 
 Here is the output BEFORE optimization:
 
 ![Alt text](before_optimization.png?raw=true "")
 
 Here is the output AFTER  optimization:
 
  ![Alt text](after_optimization.png?raw=true "")

As observed, the final result changed from 41% (loss) to 164% (profit).
