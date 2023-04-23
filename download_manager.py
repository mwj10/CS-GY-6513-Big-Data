import yfinance as yf
from datetime import date
import psycopg2
import json
import pandas as pd
from pandas_datareader import data as pdr

# custom
import db_manager as db

# connect to DB
conn = db.connectToDB();

def download(tickers,start_date,end_date,force=False):

    if force:
        # clean existent data
        db.dropTable("daily_prices",conn)
        db.dropTable("predicted_daily_prices",conn)
        db.dropTable("tickers",conn)

        # create tables
        db.createTables(conn);

    if not db.doesTableExist('tickers',conn) or force:
        # enable converting stocks data to data frame
        yf.pdr_override() # <== that's all it takes :-)
        
        # Loop ticker by ticker    
        for ticker in tickers:
            print("------------")
            print("Adding "+ticker+" to Database...")
            db.addTickerToDB(ticker,ticker) #<-- update with full name
            t_id = db.getTickerId(ticker)
            print(ticker+" index been added to the database");
            
            # download data for 10 Years!
            data_df = pdr.get_data_yahoo(ticker, start=start_date, end=end_date)
            # Storing data into Postgres
            print("Downloading Historical Data for {ticker_name}...".format(ticker_name=ticker))
            
            for datetime, row in data_df.iterrows():

                date = pd.to_datetime(datetime).date()
                open_price = "{:f}".format(row['Open'])
                high_price = "{:f}".format(row['High'])
                low_price = "{:f}".format(row['Low'])
                close_price = "{:f}".format(row['Close'])
                adj_close_price = "{:f}".format(row['Adj Close'])
                volume = "{:f}".format(row['Volume'])
                db.insertDailyPrices(date,t_id,open_price,high_price,low_price,close_price,adj_close_price,volume)
            print("{ticker} Historical Daily Prices been Downloaded".format(ticker=ticker))
        conn.commit()