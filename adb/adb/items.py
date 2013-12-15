# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html
import re
from scrapy.item import Item, Field

class Product(Item):
    url = Field()
    category = Field()
    brand = Field()
    product = Field()
    weight = Field()
    price = Field()
    retailer =  Field()


price_re = re.compile("\$([0-9]{1,8}\.[0-9]{2})")
brand_re = re.compile("^([A-Z]{2,8})\s")
weight_re = re.compile("([0-9\.]{1,5})\s*(lbs|lb|g|kg|CAPS|paks)(?i)")


def weight(name):
    match = weight_re.search(name)
    if match:
        return " ".join([i for i in match.groups()])
    else:
        return ""

def brand(name):
    b = brand_re.search(name)
    if b:
        return b.groups(0)[0]
    else:
        return ""

