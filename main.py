from datetime import date
import json
import pandas as pd
import numpy as np
from flask import Flask, request, json
import pymongo as mg
# custom libraries
import ticker_info
import db_manager as db
import download_manager as dl
import lstm

# App 
app = Flask(__name__)

# # connect to MongoDB
# mg_col_name = 'lstm_predictions';
# mgclient = mg.MongoClient("localhost", 27017) 
# mgdb = mgclient["mgdb_predictions"]
# mgcol = mgdb[mg_col_name]
# mgcol.drop() # Clean Collection on New Run
# mgcol = mgdb[mg_col_name]

@app.route("/data_view/<string:q_ticker>")
def data_view(q_ticker):
    
    conn = db.connectToDB();
    #print(db.getPredictions(q_ticker,conn).shape)
    df = db.getPrices(q_ticker,conn);
    print(df);
    json_results = {}
    for i,row in df.iterrows():
        date = row['date'].strftime('%m/%d/%Y')
        actual = float("{:.3f}".format(row['actual']))
        predicted = float("{:.3f}".format(row['predicted']))
        json_results[int(i)] = [{'date': date},{'actual':actual},{'predicted':predicted}]
    conn.close();
    return json.dumps(json_results)

@app.route("/inference/<string:q_ticker>")
def inference(q_ticker):
    
    num_of_days = request.args.get("days");
    results = None;
    if num_of_days:
        results = lstm.predict(q_ticker,numOfDays=int(num_of_days));
    else:
        results = lstm.predict(q_ticker);
    
    json_results = {}
    for i in range(len(results)):
        key = "day_{i}".format(i=i)
        value =results[i]
        json_results[key] = value
    return json.dumps(json_results)

@app.route("/train")
@app.route("/train/<string:q_ticker>")
def train_models(q_ticker=None):
    # Download data
    today = date.today()
    dl.download(ticker_info.dow30,'2013-01-01',today);

    # train on all tickers
    conn = db.connectToDB();
    
    tickers = db.getTickers(conn)
    print(tickers)
    if q_ticker is None:
        for ticker in tickers:
            print(ticker);
            lstm.train(ticker)
    else:
        lstm.train(q_ticker);

    print("DONE. :)")
    conn.close();
    
    return json.dumps({"status":"DONE"})

if __name__ == '__main__':
    app.run(debug=True)

    