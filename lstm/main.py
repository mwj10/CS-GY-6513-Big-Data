import lstm
import download_manager as dl
import db_manager as db
import ticker_info
from datetime import date
import json
import pandas as pd
import numpy as np
from flask import Flask, request, json
import pymongo as mg

# App
app = Flask(__name__)

# custom libraries

# # connect to MongoDB
# mg_col_name = 'lstm_predictions';
# mgclient = mg.MongoClient("localhost", 27017)
# mgdb = mgclient["mgdb_predictions"]
# mgcol = mgdb[mg_col_name]
# mgcol.drop() # Clean Collection on New Run
# mgcol = mgdb[mg_col_name]


@app.route("/lstm_data_view/<string:q_ticker>")
def lstm_data_view(q_ticker):

    conn = db.connectToDB()
    # print(db.getPredictions(q_ticker,conn).shape)
    df = db.getPrices(q_ticker, conn)
    print(df)
    json_results = {}
    for i, row in df.iterrows():
        date = row['date'].strftime('%m/%d/%Y')
        actual = float("{:.3f}".format(row['actual']))
        predicted = float("{:.3f}".format(row['predicted']))
        # json_results[int(i)] = [{'date': date}, {
        #     'actual': actual}, {'predicted': predicted}]
        json_results[int(i)] = {'date': date,
                                'actual': actual, 'predicted': predicted}
    conn.close()
    return json_results


@app.route("/inference/<string:q_ticker>")
def inference(q_ticker):

    num_of_days = request.args.get("days")
    results = None
    if num_of_days:
        results = lstm.predict(q_ticker, numOfDays=int(num_of_days))
    else:
        results = lstm.predict(q_ticker)

    json_results = {}
    for i in range(len(results)):
        key = "day_{i}".format(i=i)
        value = results[i]
        json_results[key] = value
    return json_results


@app.cli.command("db_seed")
@app.route("/seed")
def seed():
    # Download data
    today = date.today()
    print(today)
    # print(ticker_info.dow30)
    dl.download(ticker_info.dow30, '2013-01-01', today, force=True)
    # dl.download(ticker_info.dow30, '1900-01-01', today, force=True)
    # train on all tickers
    conn = db.connectToDB()

    tickers = db.getTickers(conn)
    print(tickers)

    for ticker in tickers:
        print(ticker)
        lstm.train(ticker)

    return {
        'message': 'News database has been seeded'
    }


@app.route("/train")
@app.route("/train/<string:q_ticker>")
def train_models(q_ticker=None):

    # train on all tickers
    conn = db.connectToDB()

    tickers = db.getTickers(conn)
    print(tickers)
    if q_ticker is None:
        for ticker in tickers:
            print(ticker)
            lstm.train(ticker)
    else:
        lstm.train(q_ticker)

    print("DONE. :)")
    conn.close()

    return json.dumps({"status": "DONE"})



@app.route("/")
@app.route("/index")
def index():
    return {"message":"LSTM service is running."}


if __name__ == '__main__':
    app.run()
