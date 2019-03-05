from model import Product, Quote, connect_to_db, db
from flask import Flask, redirect, request, render_template, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from query_helper import get_amazon_id, get_product_data
from model import Product, Quote, connect_to_db, db
from datetime import datetime
from sqlalchemy import func
import json
import math


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
 
    if (newprice == []):
        newprice = product_data['data']['AMAZON']
        newtime = product_data['data']['AMAZON_time']

    if (math.isnan(newprice[0])):
        newprice = product_data['data']['AMAZON']
        newtime = product_data['data']['AMAZON_time']

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
