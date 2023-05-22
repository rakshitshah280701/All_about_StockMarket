from concurrent.futures import process
from json import load
import numpy as np
import keras
import os
from contextlib import suppress
from pandas_datareader import data as pdr
import tensorflow as tf
import yfinance as yf
from datetime import date, timedelta
from sklearn.preprocessing import MinMaxScaler
import json
import time

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
CACHE_PATH = os.path.join(ROOT_PATH, '@cache')
ASSET_PATH = os.path.join(ROOT_PATH, 'Atemp')
STORE_PATH = os.path.join(ROOT_PATH, 'Storage')
MODEL_PATH = os.path.join(STORE_PATH, 'exported_model')
RESULT_PATH = os.path.join(ROOT_PATH, 'result.json')


# switch to cpu if gpu is unavailable in the system
if (len(tf.config.experimental.list_physical_devices('GPU'))) < 1:
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

yf.pdr_override()  # <== that's all it takes :-)

# download dataframe
today = date.today()


def stockReader(stock, start, end):
    if not end:
        end = today
    return pdr.get_data_yahoo("^NSEI", start=start, end=end)


# df = stockReader("^NSEI", "2018-01-01", end=today)


def ModelPredictor(date='2018-01-01') -> float:

    preResult = -1
    with open(file='result.json', mode='r') as f:
        readFile = f.read()
        readObject = json.loads(readFile)

        if (readObject['date'] == str(today)):
            preResult = readObject['result']

    if (preResult != -1):
        return preResult

    try:
        loaded_model = keras.models.load_model(MODEL_PATH)

        scaler = MinMaxScaler(feature_range=(0, 1))

        # get the quote
        nifty_quote = stockReader('^NSEI', start=date, end=today)

        # create a new dataframe
        new_df = nifty_quote.filter(['Close'])

        # get the last 60 day closing price values and convert the dataframe to an array
        last_range_days = new_df[-60:].values

        obj = scaler.fit(last_range_days)

        # # #scale the data to be values between 0 and 1
        last_range_days_scaled = obj.transform(last_range_days)

        # # #create an empty list
        X_test = []

        # # #APPEND THE LAST 60 DAYS
        X_test.append(last_range_days_scaled)

        # # #convert the X_test data set to np array
        X_test = np.array(X_test)

        pred_price = loaded_model.predict(X_test)
        final_price = obj.inverse_transform(pred_price)[0]
        with open(file='result.json', mode='w+') as f:
            string_res = json.dumps({
                "result": str(final_price[0]),
                "date": str(today)
            })
            f.write(string_res)

        return final_price[0]
    except(Exception) as e:
        print(e)
        print("--------- Errrorrrrrr ------")
        return -1.0


if __name__ == '__main__':
    result = ModelPredictor()
    print(result)

    # print(today)

    # print("rootPath --------->", ROOT_PATH)
