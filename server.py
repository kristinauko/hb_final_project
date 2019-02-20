from flask import Flask, redirect, request, render_template, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from jinja2 import StrictUndefined
from helper import get_amazon_id, get_product_data
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

    # if amazon_url == "": #if user submits empty string 
    #     return render_template("homepage.html") #renders /
    # else:
    amazon_id = get_amazon_id(amazon_url) #extract amazon item unique id from Amazon url
    product_payload = get_product_data(amazon_id)  #query Keepa API
    product = product_payload[0] #extracts product from product payload 

    load_products(product) 
    
    return render_template("get-prices.html", product=product, amazon_id=amazon_id)

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
    print(price_list)
    print(date_time_list)

    #This is a hardcoded string for testing if plotting works
    # date_time_list = ["2018-03-04", "2018-08-04", "2019-03-04"]
    # price_list=[5, 8, 10]

    #This is a hardcoded string for testing if plotting for large lists works
    # quotes_dictionary['date'] = ['2016-06-16', '2016-06-23', '2016-06-27', '2016-07-10', '2016-07-21', '2016-08-02', '2016-08-09', '2016-08-09', '2016-08-13', '2016-08-15', '2016-08-24', '2016-08-26', '2016-09-09', '2016-09-13', '2016-09-15', '2016-09-15', '2016-09-22', '2016-09-25', '2016-09-26', '2016-09-27', '2016-10-01', '2016-10-06', '2016-10-13', '2016-10-16', '2016-10-22', '2016-10-22', '2016-10-23', '2016-10-25', '2016-10-26', '2016-10-27', '2016-10-28', '2016-10-29', '2016-10-29', '2016-10-30', '2016-11-01', '2016-11-04', '2016-11-07', '2016-11-09', '2016-11-10', '2016-11-11', '2016-11-11', '2016-11-13', '2016-11-15', '2016-11-15', '2016-11-17', '2016-11-20', '2016-11-22', '2016-11-26', '2016-11-29', '2016-12-04', '2016-12-05', '2016-12-06', '2016-12-10', '2016-12-12', '2016-12-13', '2016-12-14', '2016-12-16', '2016-12-17', '2016-12-19', '2016-12-19', '2016-12-20', '2016-12-21', '2016-12-25', '2016-12-26', '2017-01-02', '2017-01-02', '2017-01-03', '2017-01-04', '2017-01-08', '2017-01-10', '2017-01-12', '2017-01-13', '2017-01-14', '2017-01-15', '2017-01-15', '2017-01-17', '2017-01-17', '2017-01-17', '2017-01-20', '2017-01-20', '2017-01-20', '2017-01-20', '2017-01-21', '2017-01-21', '2017-01-21', '2017-01-21', '2017-01-22', '2017-01-22', '2017-01-25', '2017-01-28', '2017-02-01', '2017-02-05', '2017-02-06', '2017-02-08', '2017-02-09', '2017-02-10', '2017-02-11', '2017-02-16', '2017-02-19', '2017-02-21', '2017-02-21', '2017-02-24', '2017-02-27', '2017-03-03', '2017-03-06', '2017-03-07', '2017-03-09', '2017-03-10', '2017-03-11', '2017-03-15', '2017-03-16', '2017-03-17', '2017-03-18', '2017-03-21', '2017-03-22', '2017-03-22', '2017-03-27', '2017-03-27', '2017-03-28', '2017-03-30', '2017-03-31', '2017-04-03', '2017-04-04', '2017-04-06', '2017-04-08', '2017-04-10', '2017-04-11', '2017-04-12', '2017-04-15', '2017-04-15', '2017-04-15', '2017-04-16', '2017-04-16', '2017-04-17', '2017-04-17', '2017-04-17', '2017-04-17', '2017-04-19', '2017-04-27', '2017-04-27', '2017-05-06', '2017-05-16', '2017-05-17', '2017-05-23', '2017-05-29', '2017-06-11', '2017-06-14', '2017-06-17', '2017-07-07', '2017-07-09', '2017-07-09', '2017-07-09', '2017-07-12', '2017-07-12', '2017-07-12', '2017-07-13', '2017-07-13', '2017-07-14', '2017-07-14', '2017-07-14', '2017-07-14', '2017-07-15', '2017-07-17', '2017-07-19', '2017-07-21', '2017-07-24', '2017-07-25', '2017-07-27', '2017-11-02', '2017-11-02', '2017-11-03', '2017-11-05', '2017-11-05', '2017-11-07', '2017-11-09', '2017-11-10', '2017-11-16', '2017-11-18', '2017-11-21', '2017-12-18', '2017-12-19', '2017-12-22', '2017-12-30', '2018-01-03', '2018-01-04', '2018-01-05', '2018-11-14', '2018-11-16', '2019-01-02', '2019-01-17', '2019-01-18', '2015-05-19', '2015-10-30', '2015-11-04', '2015-11-20', '2015-11-23', '2018-07-16', '2018-11-01', '2016-09-12', '2016-09-25', '2016-09-27', '2016-11-04', '2016-11-07', '2016-11-15', '2016-11-23', '2016-12-17', '2016-12-24', '2017-01-08', '2017-03-11', '2017-03-30', '2017-03-31', '2017-04-06', '2017-04-18', '2017-04-20', '2017-04-21', '2017-04-29', '2017-05-01', '2017-05-16', '2017-05-21', '2017-05-22', '2017-05-23', '2017-05-25', '2017-05-25', '2017-05-26', '2017-06-02', '2017-06-03', '2017-06-04', '2017-06-05', '2017-06-06', '2017-06-16', '2017-06-17', '2017-06-17', '2017-06-20', '2017-06-22', '2017-07-06', '2017-07-24', '2017-07-30', '2017-07-31', '2017-08-01', '2017-08-03', '2017-08-05', '2017-08-07', '2017-08-08', '2017-08-09', '2017-08-16', '2017-10-08', '2017-10-09', '2017-10-12', '2017-10-17', '2017-10-19', '2018-01-24', '2018-02-03', '2018-02-07', '2018-02-09', '2018-03-09', '2018-03-22', '2018-03-23', '2018-03-26', '2018-03-27', '2018-03-28', '2018-03-30', '2018-04-01', '2018-04-02', '2018-04-05', '2018-04-21', '2018-04-23', '2018-04-26', '2018-04-30', '2018-05-02', '2018-05-04', '2018-05-10', '2018-05-10', '2018-05-12', '2018-05-12', '2018-05-15', '2018-05-16', '2018-05-29', '2018-06-04', '2018-06-05', '2018-06-06', '2018-06-09', '2018-06-11', '2018-06-11', '2018-06-13', '2018-06-14', '2018-06-15', '2018-06-16', '2018-06-18', '2018-06-20', '2018-06-22', '2018-06-30', '2018-06-30', '2018-07-05', '2018-07-07', '2018-07-12', '2018-07-13', '2018-07-13', '2018-07-14', '2018-07-15', '2018-07-17', '2018-07-18', '2018-07-19', '2018-07-20', '2018-07-21', '2018-07-22', '2018-07-23', '2018-07-25', '2018-07-26', '2018-07-27', '2018-07-27', '2018-07-30', '2018-07-31', '2018-08-01', '2018-08-03', '2018-08-03', '2018-08-05', '2018-08-11', '2018-08-13', '2018-08-16', '2018-08-19', '2018-08-20', '2018-08-22', '2018-08-24', '2018-08-25', '2018-08-25', '2018-08-27', '2018-08-29', '2018-08-29', '2018-08-31', '2018-09-01', '2018-09-03', '2018-09-03', '2018-09-04', '2018-09-05', '2018-09-06', '2018-09-07', '2018-09-08', '2018-09-09', '2018-09-11', '2018-09-13', '2018-09-14', '2018-09-16', '2018-09-17', '2018-09-18', '2018-09-19', '2018-09-19', '2018-09-21', '2018-09-22', '2018-09-23', '2018-09-24', '2018-09-25', '2018-09-27', '2018-10-01', '2018-10-02', '2018-10-03', '2018-10-05', '2018-10-06', '2018-10-07', '2018-10-08', '2018-10-10', '2018-10-11', '2018-10-13', '2018-10-16', '2018-10-16', '2018-10-18', '2018-10-20', '2018-10-21', '2018-10-22', '2018-10-23', '2018-10-25', '2018-10-26', '2018-10-27', '2018-10-28', '2018-11-01', '2018-11-02', '2018-11-04', '2018-11-05', '2018-11-12', '2018-11-14', '2018-11-17', '2018-11-20', '2018-11-24', '2018-11-26', '2018-12-05', '2019-01-26', '2019-01-31', '2019-02-10', '2019-02-19', '2018-04-10', '2018-06-29', '2018-07-07', '2018-08-05', '2018-08-18', '2018-08-20', '2018-09-01', '2018-09-10', '2018-09-21', '2018-10-29', '2018-11-14', '2018-12-23']
    # quotes_dictionary['price'] = [21.99, 18.0, 14.25, 13.58, 17.4, 17.39, 17.38, 17.39, 16.85, 17.4, 16.7, 16.51, 17.72, 16.51, 16.59, 16.51, 17.15, 17.7, 17.9, 17.95, 14.01, 17.95, 17.9, 17.92, 17.15, 17.4, 16.76, 17.0, 17.4, 17.39, 16.76, 17.38, 16.6, 16.5, 16.58, 17.0, 16.68, 17.0, 16.8, 17.0, 16.8, 16.68, 16.76, 16.57, 16.65, 16.57, 16.65, 16.57, 16.65, 16.33, 16.47, 16.31, 16.24, 15.96, 14.68, 16.24, 15.7, 16.24, 16.16, 16.24, 14.68, 16.24, 16.16, 16.24, 16.16, 16.24, 16.76, 16.55, 16.47, 16.95, 16.25, 16.95, 16.47, 16.87, 16.95, 16.88, 16.93, 16.95, 17.19, 17.25, 17.2, 17.19, 17.13, 17.08, 17.05, 17.03, 17.18, 17.0, 16.99, 16.76, 16.5, 16.42, 16.5, 16.62, 16.6, 16.5, 16.4, 16.99, 16.95, 16.99, 11.99, 14.79, 16.7, 16.6, 19.53, 17.84, 17.85, 17.15, 15.79, 16.9, 16.7, 16.65, 16.5, 16.75, 17.08, 16.95, 16.99, 16.76, 16.95, 16.87, 16.73, 16.0, 16.73, 16.5, 16.25, 16.5, 16.2, 16.5, 16.25, 16.23, 16.18, 16.11, 16.05, 16.21, 16.5, 16.25, 16.24, 16.11, 15.99, 15.5, 15.99, 15.5, 15.99, 15.75, 15.99, 14.99, 15.99, 14.99, 14.9, 14.75, 14.6, 14.14, 14.6, 14.85, 14.8, 14.7, 14.55, 14.7, 14.75, 13.86, 14.75, 14.8, 16.15, 16.76, 17.95, 18.0, 18.0, 18.0, 18.0, 18.0, 18.0, 18.0, 18.0, 18.0, 18.0, 18.0, 18.0, 18.0, 18.0, 18.0, 18.0, 18.0, 18.0, 18.0, 18.0, 18.0, 69.99, 61.99, 45.99, 61.98, 61.99, 22.0, 21.0, 22.0, 21.99, 22.0, 22.0, 22.0, 89.95, 67.99, 89.95, 71.96, 72.0, 89.95, 86.45, 30.16, 86.45, 89.95, 71.95, 89.28, 89.95, 71.96, 57.25, 62.79, 71.96, 64.66, 71.96, 67.91, 64.51, 61.28, 58.22, 61.13, 58.07, 55.17, 51.13, 49.5, 48.3, 45.89, 43.6, 31.86, 30.27, 28.72, 67.46, 64.43, 60.32, 62.16, 40.89, 38.86, 36.92, 35.07, 31.65, 30.53, 30.54, 60.96, 58.97, 38.71, 38.72, 33.19, 30.97, 58.97, 53.97, 47.87, 49.13, 49.97, 45.0, 42.76, 44.91, 42.96, 45.0, 42.86, 44.9, 45.0, 43.69, 45.0, 44.24, 45.0, 44.07, 43.85, 43.74, 45.0, 43.19, 45.0, 43.08, 45.0, 42.51, 43.55, 43.83, 32.21, 30.6, 28.31, 28.09, 28.06, 28.26, 28.25, 28.37, 27.52, 26.14, 24.02, 21.68, 19.8, 19.81, 19.8, 19.79, 19.8, 19.83, 39.99, 21.86, 22.95, 23.31, 25.7, 26.99, 28.34, 29.73, 29.68, 31.16, 30.34, 33.45, 32.82, 34.46, 36.18, 34.88, 32.7, 32.64, 32.48, 32.37, 32.0, 33.54, 30.27, 29.06, 28.89, 30.33, 30.26, 30.33, 29.25, 29.93, 28.71, 30.15, 33.24, 31.79, 30.2, 30.12, 28.61, 30.04, 28.54, 29.97, 31.43, 29.86, 28.37, 28.3, 28.23, 31.12, 29.56, 31.04, 29.49, 30.96, 29.41, 30.88, 29.34, 30.81, 28.99, 29.53, 31.01, 30.81, 28.31, 29.73, 29.07, 29.09, 29.08, 29.03, 28.97, 28.91, 28.69, 28.71, 28.99, 28.69, 28.49, 29.65, 31.13, 29.57, 29.0, 29.59, 28.11, 27.42, 28.98, 27.91, 27.99, 28.5, 28.44, 27.8, 28.03, 28.11, 25.35, 24.08, 19.8, 19.91, 20.01, 39.99, 20.22, 24.0, 18.03, 18.28, 18.48, 18.24, 18.37, 18.48, 18.24, 18.57, 18.57, 18.57, 18.57]

    #Create a dictionary with keys 'date' and 'price'
    quotes_dictionary['date'] = (date_time_list)
    quotes_dictionary['price'] = (price_list)

    return jsonify(quotes_dictionary)


def load_products(product):
    """Load products to database from API request payload"""

    amazon_id = product['asin'] #amazon id for product
    name = product['title'] #name for the product

    product_entry = Product.query.filter(Product.amazon_id == amazon_id).first()

    if not product_entry:

        product_entry = Product(amazon_id=amazon_id, 
                                name=name)

        db.session.add(product_entry)
        db.session.commit()

        load_quotes(product_entry, product)  

    else: 
         update_quotes(product_entry, product)


def load_quotes(product_entry, product_data):
    """Load quotes to database from API request payload"""

    newprice = product_data['data']['NEW'] #acess new products' price history
    newtime = product_data['data']['NEW_time'] #access new products' timestamps
    
    #loop over entries
    for i in range(len(newprice)):

        current_time = newtime[i]
        current_price = newprice[i]

        quote_entry = Quote(date_time=current_time,
                            price=current_price)

        product_entry.quotes.append(quote_entry) 
    
    db.session.add(product_entry)
    db.session.commit()


def update_quotes(product_entry, product_data):
    """Update quotes to database from API request payload"""

    for quote in product_entry.quotes:
        db.session.delete(quote)
        db.session.commit()

    load_quotes(product_entry, product_data)
    
    print("Update QUOTES was called")


if __name__ == "__main__":
    connect_to_db(app)
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True 

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
