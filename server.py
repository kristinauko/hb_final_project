from flask import Flask, redirect, request, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from jinja2 import StrictUndefined
from helper import get_amazon_id, get_product_data
from model import Product, Quote, connect_to_db, db
from datetime import datetime
from sqlalchemy import func


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

    load_products(product) 
    load_quotes(product, amazon_id)  

    return render_template("get-prices.html", product=product)


def load_products(product):
    """Load products to database from API request payload"""

    print("Product")

    amazon_id = product['asin'] #amazon id for product
    name = product['title'] #name for the product


    product_entry = Product(amazon_id=amazon_id, 
                            name=name)

    db.session.add(product_entry)
    db.session.commit()


def load_quotes(product, amazon_id):
    """Load quotes to database from API request payload"""

    print("Quotes")

    db_product = Product.query.filter(Product.amazon_id == amazon_id).first() #access product_id in products table

    newprice = product['data']['NEW'] #acess new products' price history
    newpricetime = product['data']['NEW_time'] #access new products' timestamps
    
    #loop over entries
    for i in range(len(newprice)):

        current_time = newpricetime[i]
        current_price = newprice[i]

        quote_entry = Quote(product_id=db_product.product_id,
                            date_time=current_time,
                            price=current_price)

        db.session.add(quote_entry)
    db.session.commit()



if __name__ == "__main__":
    connect_to_db(app)
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True 

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
