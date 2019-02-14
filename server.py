from flask import Flask, redirect, request, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from helper import get_product_id, get_product_data
# from seed import load

#os.system("source secrets.sh")

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
    amazon_url = request.args.get("amazon-url")
    product_id = get_product_id(amazon_url)
    product = get_product_data(product_id)


    return render_template("get-prices.html", product=product)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True 

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")


