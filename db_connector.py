
import psycopg2;
def connectToDB(): 
    cred = {"host":"localhost","port":"5432","database":"postgres","user":"postgres","password":"123"}
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(
        host=cred["host"],
        port=cred['port'],
        database=cred["database"],
        user=cred["user"],
        password=cred["password"])
    return conn
    # create a cursor
    cur = conn.cursor()


# connectToDB();
# # execute a statement
# print('PostgreSQL database version:')
# cur.execute('SELECT version()')
# # display the PostgreSQL database server version
# db_version = cur.fetchone()