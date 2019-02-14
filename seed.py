import datetime
from sqlalchemy import func

from model import Product, Quote, connect_to_db, db
from server import app

# Keepa API: Products is a list of product data with one entry per successful 
# result from the Keepa server. 
the_product = product[0]

def load_products(products):
    """Load products from API request payload"""

    print("Product")

    amazon_id = the_product['asin']
    name = the_product['title']


    product = Product(amazon_id=amazon_id, 
                name=name)

    db.session.add(product)

    db.session.commit()

def load_quotes(products):
    """Load quotes from API request payload"""

    print("Quotes")

    # Access new price history and associated time data
    newprice = the_product['data']['NEW']
    newpricetime = the_product['data']['NEW_time']
    
    #loop over entries and 
    for i in range(365):

        current_time = newpricetime[i]
        current_price = newprice[i]

        quote = Quote(date_time=current_time,
                    price=current_price)

        db.session.add(quote)

db.session.commit()
       



if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()


    load_products()
    load_quotes()
