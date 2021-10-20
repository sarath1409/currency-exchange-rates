import json, logging, sqlite3, requests
from datetime import date
from datetime import datetime
from time import time
from time import mktime as mktime

logging.basicConfig(filename='./app_log.log', level=logging.INFO,
                    format='%(asctime)s || %(levelname)s || %(message)s')

try:
    conn = sqlite3.connect('./exchangeData.db', check_same_thread=False)
    cur = conn.cursor()
except Exception as e:
    logging.error('Error while connecting to DB: {}'.format(e))

url = 'https://openexchangerates.org/api/historical/{}.json?app_id=878bc4b5f63e4067b04e768bd76f47e2'

def create_table():
    with conn:
        try:
            cur.execute("DROP TABLE exchangeRates")
        except Exception as e:
            logging.error('Unable to Drop the table, Table might not be present in the system')
            logging.error(e)
        cur.execute(""" CREATE TABLE exchangeRates (
                timestamp TEXT PRIMARY KEY,
                afn	REAL, ars	REAL, aud	REAL,
                bdt	REAL, eur	REAL, cad	REAL,
                cny	REAL, cup	REAL, dkk	REAL,
                egp	REAL, inr	REAL, jpy	REAL,
                myr	REAL, mxn	REAL, npr	REAL,
                kpw	REAL, pkr	REAL, zar	REAL,
                sgd	REAL, krw	REAL, chf	REAL,
                gbp	REAL, aed	REAL, usd	REAL
            );""")

def insert_exchange_data(missing_date,data):
    try:
        with conn:
            cur.execute("""
            INSERT INTO exchangeRates 
            VALUES ( :timestamp,
            :afn, :ars, :aud, 
            :bdt, :eur, :cad, 
            :cny, :cup, :dkk, 
            :egp, :inr, :aed,
            :jpy, :myr, :mxn, 
            :npr, :kpw, :pkr, 
            :zar, :sgd, :krw, 
            :chf, :gbp, :usd)""",
            {'timestamp':missing_date,
            'afn':data['rates']['AFN'], 'ars':data['rates']['ARS'], 'aud':data['rates']['AUD'], 
            'bdt':data['rates']['BDT'], 'eur':data['rates']['EUR'], 'cad':data['rates']['CAD'], 
            'cny':data['rates']['CNY'], 'cup':data['rates']['CUP'], 'dkk':data['rates']['DKK'], 
            'egp':data['rates']['EGP'], 'aed':data['rates']['AED'], 'inr':data['rates']['INR'], 
            'jpy':data['rates']['JPY'], 'myr':data['rates']['MYR'], 'mxn':data['rates']['MXN'], 
            'npr':data['rates']['NPR'], 'kpw':data['rates']['KPW'], 'pkr':data['rates']['PKR'], 
            'zar':data['rates']['ZAR'], 'sgd':data['rates']['SGD'], 'krw':data['rates']['KRW'], 
            'chf':data['rates']['CHF'], 'gbp':data['rates']['GBP'], 'usd':data['rates']['USD']}
            )
    except Exception as e:
        logging.error('Error while inserting data:{}'.format(e))

def fetch_exchange_data(timestamp):
    try:
        cur.execute("""SELECT * 
                    FROM exchangeRates
                    WHERE timestamp = :timestamp""",{'timestamp':timestamp})
        ret = cur.fetchone()
        return ret
    except Exception as e:
        logging.error('Error at fetching exchange Data:{}'.format(e))

def fetch_period_data(timestamp,days):
    
    date_val = int(mktime(datetime.strptime(timestamp,"%Y-%m-%d").timetuple()))
    results,return_data = [],[]
    prev_date = date_val

    try:
        for _ in range(days):
            cur.execute("""SELECT * 
                    FROM exchangeRates
                    WHERE timestamp = :timestamp""",{'timestamp':str(date.fromtimestamp(prev_date))})
            prev_date = prev_date - 86400
            results.append(cur.fetchone())

        row_headers=[x[0] for x in cur.description] 

        for result in results:
            return_data.append(dict(zip(row_headers,result)))
        return return_data
    except Exception as e:
        logging.error('Error at fetching period Data:{}'.format(e))

def get_columns():
    try:
        cur.execute("SELECT * FROM exchangeRates LIMIT 1")
        row_headers=[x[0] for x in cur.description]
        return row_headers
    except Exception as e:
        logging.error("Unable to fetch data: {}".format(e))


def fetch_all_data():
    cur.execute("""SELECT * FROM exchangeRates""")
    row_headers=[x[0] for x in cur.description] 
    rv = cur.fetchall()
    return_data = []
    for result in rv:
        return_data.append(dict(zip(row_headers,result)))
    return json.dumps(return_data)