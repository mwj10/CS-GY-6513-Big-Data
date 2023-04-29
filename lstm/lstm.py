from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import joblib
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
# custom libraries
import db_manager as db


def getLSTM():
    # Architecture LSTM
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(60, 1)))
    model.add(LSTM(50, return_sequences=True))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')

    return model


def getData(ticker):
    conn = db.connectToDB()
    df = db.getDailyPrices(ticker, conn=conn)
    # Keep only close
    conn.close()
    return df['close']

# convert an array of values into dataset matrix


def create_dataset(dataset, time_step=1):
    X, Y = [], []
    for i in range(len(dataset)-time_step-1):
        X.append(dataset[i:(i+time_step), 0])
        Y.append(dataset[i+time_step, 0])
    return np.array(X), np.array(Y)


def inversePredictionResult(results, scaler):
    inversed_results = scaler.inverse_transform(results)
    inversed_results = inversed_results.reshape(1, -1).tolist()[0]
    return inversed_results


def train(ticker, look_back=60, epochs=1, batch_size=64):

    print("#### Training {ticker_name} model...".format(
        ticker_name=ticker)+" ####")
    # Data Transformation
    df = getData(ticker)
    scaler = MinMaxScaler(feature_range=(0, 1))
    df2 = scaler.fit_transform(np.array(df).reshape(-1, 1))

    # Split Training and Test Datasets
    train_size = int(len(df2)*0.65)
    test_size = len(df2)-train_size
    train_data, test_data = df2[0:train_size, :], df2[train_size:len(df2), :1]

    # Split datasets into input and targets
    X_train, y_train = create_dataset(train_data, look_back)
    X_test, y_test = create_dataset(test_data, look_back)

    # Reshape to include additional dimension
    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
    X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

    # Fitting model
    model = getLSTM()
    model.fit(X_train, y_train, validation_data=(X_test, y_test),
              epochs=epochs, batch_size=batch_size, verbose=1)

    # Saving Model
    print("Saving model...")
    model.save("models/"+ticker)
    #joblib.dump(scaler, '{scaler}.gz'.format(scaler=ticker));

    train_predict = model.predict(X_train)
    test_predict = model.predict(X_test)

    train_predict = scaler.inverse_transform(train_predict)
    train_predict = train_predict.reshape(
        1, train_predict.shape[0]).tolist()[0]
    test_predict = scaler.inverse_transform(test_predict)
    test_predict = test_predict.reshape(1, test_predict.shape[0]).tolist()[0]

    conn = db.connectToDB()
    df = db.getDailyPrices(ticker, conn=conn)
    df = df['date']
    df = df[df.shape[0]-len(test_predict):df.shape[0]]
    i = 0
    for d in df:
        db.insertPrediction(d, ticker, test_predict[i], conn)
        i += 1


def predict(ticker, numOfDays=5, look_back=60):

    print("#### Predicting Next {num} for {ticker} ####".format(
        num=numOfDays, ticker=ticker))
    print("Fetching data ...")
    # load data
    stock_prices = getData(ticker)
    scaler = MinMaxScaler(feature_range=(0, 1))
    stock_prices = scaler.fit_transform(np.array(stock_prices).reshape(-1, 1))
    # Use only last 60 days
    i = len(stock_prices)-look_back
    x_input = stock_prices[i:, :1].reshape(1, -1)
    temp_input = list(x_input)
    temp_input = temp_input[0].tolist()

    print("Loading Model...")
    # load model and scaler
    model = tf.keras.models.load_model("models/"+ticker)

    print("Predicting...")
    # Predicting ...
    lst_output = []
    n_steps = look_back
    i = 0
    while(i < numOfDays):
        if(len(temp_input) > look_back):
            # print(temp_input)
            x_input = np.array(temp_input[1:])
            #print("{} day input {}".format(i,x_input))
            x_input = x_input.reshape(1, -1)
            x_input = x_input.reshape((1, n_steps, 1))
            # print(x_input)
            yhat = model.predict(x_input, verbose=0)
            #print("{} day output {}".format(i,yhat))
            temp_input.extend(yhat[0].tolist())
            temp_input = temp_input[1:]
            # print(temp_input)
            lst_output.extend(yhat.tolist())
            i = i+1
        else:
            x_input = x_input.reshape((1, n_steps, 1))
            yhat = model.predict(x_input, verbose=0)
            # print(yhat[0])
            temp_input.extend(yhat[0].tolist())
            # print(len(temp_input))
            lst_output.extend(yhat.tolist())
            i = i+1

    #scaler = MinMaxScaler(feature_range=(0,1))
    results = inversePredictionResult(lst_output, scaler)

    print("Done.")
    return results

# #train('AAPL');
# results = predict('AAPL')
# print(results);
