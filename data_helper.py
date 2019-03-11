import pandas as pd

import math
import itertools
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

    pd_future_dates = pd.date_range(pd.to_datetime("today"), periods=list_length + 1, freq='W').strftime("%m-%d-%Y")

    future_dates = []

    for item in pd_future_dates:
        future_dates.append(item)

    return future_dates


def get_python_list(predictions):
    """Take numpy array and return Python list"""

    merged_prediction = list(itertools.chain.from_iterable(predictions))

    python_list = []

    for item in merged_prediction:
        pyval = item.item()
        rounded_value = round(pyval, 2)
        python_list.append(rounded_value)
    return python_list

def get_pd_dataframe(date_time_list, price_list):
    """Take two list of strings and create pandas DataFrame"""

    index_range = range(len(date_time_list))

    df = pd.DataFrame(index=index_range,columns=['Date', 'Price'])

    for i in index_range:
        df['Date'][i] = date_time_list[i]
        df['Price'][i] = price_list[i]

    return df


def normalize_data(df):
    """Take original pd dataset and create price averages for weeks, return pd dataset"""

    original_index = 0
    normalized_series = []
    nex_index = 0

    #loop through pandas dates, starting with the earliest date and divide time into periods (weeks), get average of prices
    for period_end in pd.date_range(start=df.min().Date, end=df.max().Date, freq='W', normalize=True):
        price_sum = 0
        num_prices = 0
        last_price = 0
        
        #while loop: continue while index is less then lenght of df, drop the time and compare date to the end of the period
        while original_index < len(df) and pd.to_datetime(df.loc[original_index].Date).normalize() <= period_end:
            
            last_price = df.loc[original_index]["Price"]
            price_sum += last_price
            num_prices +=1
            original_index +=1

        #if sum of prices for the week is zero, use last week price as an average
        if price_sum == 0:
            average_price_point = (period_end, normalized_series[-1][2],normalized_series[-1][2])
           
        #otherwise average price point is the average of all period prices
        else:
            average_price_point = (period_end, price_sum / num_prices, last_price)

        #append average price point to normalized series
        normalized_series.append(average_price_point)
        original_index += 1
        
    print("Normalized to {0} {1} intervals".format(len(normalized_series), "W"))

    index_range = range(len(normalized_series))

    df = pd.DataFrame(index=index_range,columns=['Date', 'Price'])

    for i in index_range:
        df['Date'][i] = normalized_series[i][0]
        df['Price'][i] = normalized_series[i][1]

    return df

    
