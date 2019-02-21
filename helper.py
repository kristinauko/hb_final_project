import keepaAPI
import os

#os.system("source secrets.sh")

#get Keepa API acessskey from secrets.sh
accesskey = os.environ["API_KEY"]


def get_amazon_id(amazon_url):
    """ When Amazon url string is presented in the search field, return 
    product id
    """

    amazon_url.replace("?", "/")
    split_url_list = amazon_url.split("/")

    for i in range(0, len(split_url_list) - 1):

        if split_url_list[i] == "dp":
            amazon_id = split_url_list[i+1]
            print(amazon_id)
            return amazon_id
        elif split_url_list[i] == "product":
            amazon_id = split_url_list[i+1]
            print(amazon_id)
            return amazon_id

# https://www.amazon.com/dp/B07N1H4YFH?aaxitk=9u7mnLyUfNJip2hHgCgrKw
def get_product_data(amazon_id):
    """ Send request to get all product data"""
    
    api = keepaAPI.API(accesskey)
    products = api.ProductQuery(amazon_id)

    return products



