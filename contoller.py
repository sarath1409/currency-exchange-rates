import requests, time, logging
from datetime import date, datetime
from model import fetch_exchange_data, insert_exchange_data

logging.basicConfig(filename='./app_log.log', level=logging.INFO,
                    format='%(asctime)s || %(levelname)s || %(message)s')

url = 'https://openexchangerates.org/api/historical/{}.json?app_id=878bc4b5f63e4067b04e768bd76f47e2'

def check_date_range(date_value):
    if type(date_value) == type(""):
        date_value = int(time.mktime(datetime.strptime(date_value,"%Y-%m-%d").timetuple()))
    if (date_value <= time.time()) and (date.fromisoformat('1999-01-01') <= date.today()):
        return True
    return False

def check_data(date_value,days):
    # check range of the timestamp: it should not be a future date and must be greater than 01-01-1999
    if (check_date_range(date_value)):

        logging.info('Date is within valid range')

        res = fetch_exchange_data(date_value)
        timestamp = int(time.mktime(datetime.strptime(date_value,"%Y-%m-%d").timetuple()))

        missing_dates = [str(date.fromtimestamp(timestamp))] if res == None else []
        msg = 'Missing date in DB found: {}.'.format(date.fromtimestamp(timestamp)) if(len(missing_dates) > 0) else 'Dates are found in DB, no need to request'
        logging.info(msg)

        prev_day = timestamp # variable to store previous dates timestamp
        for _ in range(days):
            prev_day = prev_day - 86400
            if check_date_range(prev_day):
                response = fetch_exchange_data(prev_day)
                if response == None:
                    logging.info('{} date is missing in the DB, adding to missing dates list to request'.format(date.fromtimestamp(prev_day)))
                    missing_date = str(date.fromtimestamp(prev_day))
                    missing_dates.append(missing_date)

        return missing_dates

def populate_missing_data(missing_dates):
    if len(missing_dates) == 0:
        logging.info('No missing dates for this request.')
        return False
    else:
        for missing_date in missing_dates:
            if (check_date_range(missing_date) and fetch_exchange_data(missing_date) == None): 
                # check if the date comes under the range and if the date is not present in table
                data = requests.get(url.format(missing_date))
                data = data.json()
                insert_exchange_data(missing_date,data)
        return True