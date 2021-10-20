from flask import Flask, url_for, render_template, redirect, request
from datetime import date
import logging, requests,json
from model import fetch_exchange_data,fetch_all_data,fetch_period_data, get_columns
from contoller import check_date_range, check_data, populate_missing_data

logging.basicConfig(filename='./app_log.log', level=logging.INFO,
                    format='%(asctime)s || %(levelname)s || %(message)s')

'https://openexchangerates.org/api/historical/2021-09-26.json?app_id=878bc4b5f63e4067b04e768bd76f47e2'

app = Flask(__name__)

@app.route('/')
def home():
    logging.info('Redirected to Homepage')
    today = str(date.today())
    columns = get_columns()
    columns.remove('usd')
    columns.remove('timestamp')
    return render_template("home.html", title="Exchange Rates", today=today, columns=columns)

@app.route('/exchangeData',methods=['POST'])
def exchangeData():
    date_value = request.form.get("date")
    no_of_days = request.form.get("days")
    currency = request.form.get("currency")
    logging.info('Fetching exchange data')
    no_of_days = int(no_of_days)
    
    if no_of_days>7 or no_of_days<1:
        no_of_days = 7
    # check range of the timestamp: it should not be a future date and must be greater than 01-01-1999
    if (check_date_range(date_value)) :
        res = check_data(date_value,no_of_days)
        data_populate_flag = populate_missing_data(res) #True if data populated now false if data is already present.
        msg = 'Data unavailable in system, now requested using api.' if(data_populate_flag) else 'Data already present, fetching from DB'
        logging.info(msg)
    return redirect(url_for('fetchPeriod', dateValue = date_value, noOfDays=no_of_days, currency=currency ))

@app.route('/test/<timestamp>',methods=['GET'])
def test(timestamp):
    return str(fetch_exchange_data(timestamp) != None)

@app.route('/test1', methods=['GET', 'POST'])
def index():
    return {'snippets':['blah','blaha']}

@app.route('/fetchPeriod/<string:dateValue>/<int:noOfDays>',methods=['GET'])
def fetchPeriod(dateValue, noOfDays):
    logging.info('Fetching data for {} date, for {} of days'.format(dateValue,noOfDays))
    data = fetch_period_data(dateValue, noOfDays)
    columns = get_columns()
    return render_template('exchange_rates.html', data=data, columns=columns, noOfDays=noOfDays)

@app.route('/alldata/',methods=['GET'])
def alldata():
    # return {'snippets':['blah','blaha']}
    a= fetch_all_data()
    a =json.loads(a)
    return {'response':a}
