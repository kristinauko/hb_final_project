from flask import Flask, redirect, request, render_template, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from jinja2 import StrictUndefined
from query_helper import get_amazon_id, get_product_data
from database_helper import load_products, load_quotes, update_quotes
from model import Product, Quote, connect_to_db, db
from datetime import datetime
from sqlalchemy import func
import json
import math


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

    date_time_list = []
    price_list = []
    quotes_dictionary = {}

    #Take product_quotes list and extract two lists - price_list and date_time_list
    #Ignore NaN prices and coresponding timestamps
    for item in product_quotes_list:
        if not math.isnan(item.price):
            price_list.append(item.price)
            timestamp = item.date_time.strftime("%Y-%m-%d")
            date_time_list.append(timestamp)

    min_price = min(price_list, default="Unknown for this product")

    #https://www.amazon.com/Nutri-Lock-Vacuum-Sealer-Bags-Bags/dp/B07H22363S/ref=sr_1_sc_3?s=sporting-goods&ie=UTF8&qid=1550781069&sr=1-3-spell&keywords=galon+ziplock+bags


    #This is a hardcoded string for testing if pricing/dates plotting works
    # date_time_list = ["2018-03-04", "2018-08-04", "2019-03-04"]
    # price_list=[5, 8, 10]

    #This is a hardcoded string for testing if future prices/dates plotting works
    prediction_dates_list = ["2018-03-04", "2018-08-04", "2019-03-04"]
    prediction_prices_list=[5, 8, 10]
    
    #Create a dictionary with keys 'date' and 'price'
    quotes_dictionary['date'] = (date_time_list)
    quotes_dictionary['price'] = (price_list)
    quotes_dictionary['prediction_dates'] = (prediction_dates_list)
    quotes_dictionary['prediction_prices'] = (prediction_prices_list)
    quotes_dictionary['min_price'] = (min_price)

    return jsonify(quotes_dictionary)





if __name__ == "__main__":
    connect_to_db(app)
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True 

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
