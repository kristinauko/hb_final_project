from flask import Flask, redirect, request, render_template, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from jinja2 import StrictUndefined
from datetime import datetime
from sqlalchemy import func

import pandas as pd
import json
import math

from model import Product, Quote, connect_to_db, db
from database_helper import load_products, load_quotes, update_quotes
from query_helper import get_amazon_id, get_product_data
from data_helper import clean_data, populate_future_dates, get_pd_dataframe, normalize_data
from training import get_prediction

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True


app.secret_key = "ABC"


@app.route("/")
def home_page():
    """Renders template homepage.html"""
        
    return render_template('homepage.html')


@app.route("/get-prices")
def get_prices():
    """Renders template for displaying prices"""

    amazon_url = request.args.get("amazon-url") #get input which is Amazon url

    amazon_id = get_amazon_id(amazon_url) #extract amazon item unique id from Amazon url

    if Product.query.filter(Product.amazon_id==amazon_id).first():
        name = Product.query.filter(Product.amazon_id==amazon_id).first().name

    else:
        product_payload = get_product_data(amazon_id)  #query Keepa API
        product = product_payload[0] #extracts product from product payload 
        name = product['title']

        load_products(product) 
    
    return render_template("get-prices.html", name=name, amazon_id=amazon_id)


@app.route("/get-prices.json")
def create_json():

    #Get amazon_id from route "/get-prices"
    amazon_id = request.args.get('amazon_id')

    #Get product quotes list: join Product and Quote tables, get entries with specific amazon_id from Products table
    product_quotes_list = Quote.query.join(Product, Quote.product_id==Product.product_id).filter(Product.amazon_id==amazon_id).all()

    #print(product_quotes_list)

    quotes_dictionary = {}

    price_list, date_time_list = clean_data(product_quotes_list)

    min_price = min(price_list, default="Unknown for this product")

    df = get_pd_dataframe(date_time_list, price_list)

    #add missing data points for the model: week based prediction
    df = normalize_data(df)

    prediction_prices_list= get_prediction(amazon_id, df)

    prediction_dates_list = populate_future_dates(len(prediction_prices_list))
    
    #Create a dictionary with keys 'date' and 'price'
    quotes_dictionary['date'] = df['Date'].dt.strftime("%m-%d-%Y").tolist()
    quotes_dictionary['price'] = df['Price'].tolist()
    quotes_dictionary['prediction_dates'] = prediction_dates_list[1:]
    quotes_dictionary['prediction_prices'] = prediction_prices_list
    quotes_dictionary['min_price'] = min_price

    return jsonify(quotes_dictionary)


if __name__ == "__main__":
    connect_to_db(app)
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = False 

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
