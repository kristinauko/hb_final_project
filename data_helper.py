import pandas as pd

import math
from datetime import datetime



def clean_data(product_quotes_list):
    #Take product_quotes list from database and extract two lists - price_list and date_time_list
    #Ignore NaN prices and coresponding timestamps

    price_list = []
    date_time_list = []

    for item in product_quotes_list:
        if not math.isnan(item.price):
            price_list.append(item.price)
            timestamp = item.date_time.strftime("%Y-%m-%d")
            date_time_list.append(timestamp)

    return price_list, date_time_list


def populate_future_dates(list_length):
    """Take the length of predicted price list and get the same amount of dates for the future"""

    pd_future_dates = pd.date_range(pd.to_datetime("today"), periods=list_length + 1, freq='D').strftime("%Y-%m-%d")

    future_dates = []

    for item in pd_future_dates:
        future_dates.append(item)

    return future_dates




    
