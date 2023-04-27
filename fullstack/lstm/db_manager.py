
import psycopg2
import pandas as pd

conn = None
cur = None


def connectToDB():
    global conn
    global cur

    cred = {"host": "localhost", "port": "5433", "database": "lstm",
            "user": "postgres", "password": "postgres"}
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(
        host=cred["host"],
        port=cred['port'],
        database=cred["database"],
        user=cred["user"],
        password=cred["password"])
    print("Connected !")
    cur = conn.cursor()
    return conn


def doesTableExist(tablename, conn):
    cur = conn.cursor()
    checkExistCmd = "select exists(select * from information_schema.tables where table_name='"+tablename+"')"
    cur.execute(checkExistCmd)
    return cur.fetchone()[0]


def dropTable(tablename, conn):
    cur = conn.cursor()
    if doesTableExist(tablename, conn):
        dropCmd = "DROP TABLE "+tablename+";"
        cur.execute(dropCmd)
        conn.commit()


def addTickerToDB(ticker_name, ticker_fullname, conn):
    cur = conn.cursor()
    insertCmd = "INSERT INTO tickers (t_name,t_full_name) VALUES('" + \
        ticker_name+"','"+ticker_fullname+"') RETURNING *"
    cur.execute(insertCmd)
    res = cur.fetchone()
    return not res is None


def getTickerId(ticker_name, conn=None):
    sqlCmd = "SELECT * FROM tickers WHERE t_name = '"+ticker_name+"'"
    cur.execute(sqlCmd)
    res = cur.fetchone()
    return res[0]


def insertDailyPrices(date, ticker_id, open, low, high, close, adj_close, volume):
    insertCmd = """INSERT INTO daily_prices(date,ticker_id,open,low,high,close,adj_close,volume)
                VALUES('{date}',{ticker_id},{open},{low},{high},
                {close},{adj_close},{volume}) RETURNING *
                """.format(date=date, ticker_id=ticker_id,
                           open=open, high=high, low=low,
                           close=close, adj_close=adj_close, volume=volume)
    cur.execute(insertCmd)
    res = cur.fetchone()
    conn.commit()
    return not res is None


def insertPrediction(date, ticker, prediction, conn):
    ticker_id = getTickerId(ticker, conn)
    insertCmd = """INSERT INTO predicted_daily_prices(date,ticker_id,predicted)
                VALUES('{date}',{ticker_id},{predicted}) RETURNING *
                """.format(date=date, ticker_id=ticker_id, predicted=prediction)
    cur = conn.cursor()
    cur.execute(insertCmd)
    res = cur.fetchone()
    conn.commit()
    return not res is None


def getPredictions(ticker, conn, date=None):
    ticker_id = getTickerId(ticker, conn)
    cur = conn.cursor()
    if date == None:
        sqlCmd = "SELECT * FROM predicted_daily_prices WHERE ticker_id = {ticker_id}".format(
            ticker_id=ticker_id)
        return pd.read_sql(sqlCmd, con=conn)
    else:
        sqlCmd = "SELECT * FROM predicted_daily_prices WHERE ticker_id = {ticker_id} AND date={date}".format(
            ticker_id=ticker_id, date=date)
        cur.execute(sqlCmd)
        res = cur.fetchone()
        return res[0]


def getPrices(ticker, conn, date=None):
    ticker_id = getTickerId(ticker, conn)
    cur = conn.cursor()
    if date == None:
        sqlCmd = """
                 SELECT t.t_id AS id, t.t_name AS name, t.t_full_name AS full_name, dp.date as date, dp.close as actual,
                 dp.open, dp.high, dp.low, dp.adj_close, dp.volume, pdp.predicted
                 FROM tickers AS t, daily_prices AS dp, predicted_daily_prices AS pdp 
                 WHERE t.t_id=dp.ticker_id AND t.t_id=pdp.ticker_id AND dp.date=pdp.date
                 AND t.t_id = {t_id}""".format(t_id=ticker_id)
        return pd.read_sql(sqlCmd, con=conn)
    else:
        sqlCmd = """
                    SELECT t.t_id AS id, t.t_name AS name, t.t_full_name AS full_name, dp.date as date, dp.close as actual,
                    dp.open, dp.high, dp.low, dp.adj_close, dp.volume, pdp.predicted
                    WHERE t.t_id=dp.ticker_id AND t.t_id=pdp.ticker_id AND dp.date=pdp.date 
                    AND t.t_id = {t_id} AND date={date}""".format(t_id=ticker_id, date=date)
        cur.execute(sqlCmd)
        res = cur.fetchone()
        return res[0]


def getTickers(conn):
    sqlCmd = "SELECT t_name FROM tickers"
    return pd.read_sql(sqlCmd, con=conn)['t_name']


def getDailyPrices(ticker, date=None, conn=None):
    ticker_id = getTickerId(ticker, conn)
    sqlCmd = ""
    if date == None:
        sqlCmd = """SELECT date,t_name as ticker,open,close,low,high,volume 
                    FROM daily_prices,tickers 
                    WHERE t_id=ticker_id AND t_id = {t_id}
                    """.format(t_id=ticker_id)
    else:
        sqlCmd = """SELECT date,t_name as ticker,open,close,low,high,volume 
                    FROM daily_prices,tickers 
                    WHERE t_id=ticker_id AND t_id={t_id} AND date={date}
                    """.format(t_id=ticker_id, date=date)
    return pd.read_sql(sqlCmd, con=conn)


def createTables(conn):
    # tickers Table
    createCmd = """ CREATE TABLE tickers (
                    t_id SERIAL PRIMARY KEY,
                    t_name VARCHAR(5),
                    t_full_name VARCHAR(255)
                    )
                """
    cur.execute(createCmd)
    conn.commit()

    # Daily Prices Table
    createCmd = """ CREATE TABLE daily_prices (
                    date DATE,
                    ticker_id SERIAL,
                    open DECIMAL,
                    high DECIMAL,
                    low DECIMAL,
                    close DECIMAL,
                    adj_close DECIMAL,
                    volume REAL,
                    PRIMARY KEY(date,ticker_id),
                    CONSTRAINT fk_dp_ticker FOREIGN KEY(ticker_id) REFERENCES tickers(t_id)
                    )
                """

    cur.execute(createCmd)
    conn.commit()

    # Predict Prices
    createCmd = """ CREATE TABLE predicted_daily_prices (
                    date DATE,
                    ticker_id SERIAL,
                    predicted DECIMAL,
                    PRIMARY KEY(date,ticker_id),
                    CONSTRAINT fk_pdp_ticker FOREIGN KEY(ticker_id) REFERENCES tickers(t_id)
                    )
                """

    cur.execute(createCmd)
    conn.commit()
