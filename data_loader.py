import yfinance as yf
from tickers import DOW30
from datetime import date
import psycopg2
import json
import pandas as pd
import numpy as np
from pandas_datareader import data as pdr
# Import the plotting library
import matplotlib.pyplot as plt

dow_30tickers = ['AAPL','AMGN','AXP','BP','CAT','CRM','CSCO','CVX','DIS','DOW','GS','HD','HON','IBM',
'INTC','JNJ','JPM','KO','MCD','MMM','MRK','MSFT','NKE','PG','TRV','UNH','V','VZ','WBA','WMT']

print(len(dow_30tickers))

today = date.today()

START_DATE = '2013-01-01'
END_DATE = today

msft = yf.Ticker(DOW30.MSFT.name)

#data = yf.download('AAPL','2013-01-01','2019-08-01')
yf.pdr_override() # <== that's all it takes :-)
data_df = pdr.get_data_yahoo("SPY", start=START_DATE, end=END_DATE)
print(len(data_df));
for index, row in data_df.iterrows():
    print("---- New Row ----")
    print(index);
    print(row);
    break;

# Plot the close price of the AAPL
# data['Adj Close'].plot()
# plt.show()