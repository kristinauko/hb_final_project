from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask, redirect, request, render_template, session


db = SQLAlchemy()


class Product(db.Model):
    """Product model."""

    __tablename__ = "products"

    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amazon_id = db.Column(db.String(25), nullable=False,)
    name = db.Column(db.String(300), nullable=False,)

    quotes = db.relationship('Quote', backref='product')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<Product product_id={self.product_id} 
                   amazon_id={self.amazon_id} 
                   name={self.name}"""


class Quote(db.Model):
    """Quote model."""
    __tablename__ = "quotes"

    quote_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'),)
    date_time = db.Column(db.DateTime,)
    price = db.Column(db.Float,)


    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<Quote quote_id={self.quote_id}
                    product_id={self.product_id} 
                   date_time={self.date_time} 
                   price={self.price}"""

   
##############################################################################
# Helper functions
    

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///productsandquotes'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # If we run this module interactively,
    # we are able to work with the database directly.
    from server import app

    connect_to_db(app)
    print("Connected to DB.")