from flask import Flask, redirect, request, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
import keepaAPI
import os
from helper import get_product_id, get_product_data

#os.system("source secrets.sh")

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

app.secret_key = "ABC"

accesskey = os.environ["API_KEY"]


@app.route("/")
def home_page():
    """Renders template homepage.html"""
        
    return render_template('homepage.html')

@app.route("/get-prices")
def get_prices():
    """Renders template for displaying prices"""
    amazon_url = request.args.get("amazon-url")
    product_id = get_product_id(amazon_url)
    product = get_product_data(product_id)


    return render_template("get-prices.html", product=product)


def get_product_id(amazon_url):
    """ When Amazon url string is presented in the search field, return product id"""
    amazon_url.replace("?", "/")
    split_url_list = amazon_url.split("/")

    for i in range(0, len(split_url_list) - 1):
        if split_url_list[i] == "dp":
            product_id = split_url_list[i+1]
            return product_id


def get_product_data(product_id):
    """ Send request to get all product data"""
    
    api = keepaAPI.API(accesskey)

    products = api.ProductQuery(product_id)

    return products[0]


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = False

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")


