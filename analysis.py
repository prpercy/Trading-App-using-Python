import yfinance as yf
from finta import TA
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')

class Database():
    def __init__(self, ticker):
        self.ticker = ticker
        data = yf.download(ticker, start="2019-01-01", end="2022-10-01")
        self.df = pd.DataFrame(data)
        self.df['Date'] = pd.to_datetime(self.df.index)
        pd.set_option('display.max_columns', None)
        
    def quote(self):
        return self.df
    
db = Database('GOOG')
df = db.quote()

df['SMA'] = TA.SMA(df, 50)

print(df)

plt.figure(figsize=(12,7))
plt.plot('Close', data=df, label='Close Price Google', color ='blue', linewidth=1)
plt.plot('SMA', data=df, label='Simple Moving Average', color='Red', linewidth=1)

plt.xlabel('Date')
plt.ylabel('Stock Price')
plt.legend()
plt.show()
