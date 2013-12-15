import re

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from adb.items import Product, weight, brand

"""
 ################################################################
WARNING: This is an example of a spider pointing to a bogus domain
 ################################################################
"""

class ExampleSpider(CrawlSpider):
    name = 'example'
    allowed_domains = ['example.com']
    start_urls = ['http://www.example.com/']

    rules = (
        Rule(SgmlLinkExtractor(
                allow=[ r''],
                deny=[r'contact_us.html',
                      r'page.html?id=1',
                      r'index.php?main_page=account',
                      r'index.php?main_page=shopping_cart',
                      ]
                ), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        items = hxs.select(
            '//div[contains(@class, "centerBoxContentsProducts")]')
        products = []
        for item in items:
            p = Product()
            p['retailer'] = self.name
            p['category'] = None
            p['brand'] = None
            p['product'] = item.select(
                './/h3[@class="itemTitle"]/a/text()').extract().pop()
            p['url'] = item.select(
                './/h3[@class="itemTitle"]/a/@href').extract().pop()
            p['weight'] = weight(p['product'])
            p['price'] = item.select(
                './/span[@class="productSpecialPrice"]/text()'
                ).re("\$([0-9]{1,8}\.[0-9]{2})").pop()
            products.append(p)
        return products
