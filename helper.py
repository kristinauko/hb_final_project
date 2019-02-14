

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
