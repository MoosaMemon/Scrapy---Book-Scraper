# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BookItem(scrapy.Item):
    title = scrapy.Field()
    url_of_prod = scrapy.Field()
    product_description = scrapy.Field()
    product_category = scrapy.Field()
    upc = scrapy.Field()
    product_type = scrapy.Field()
    rating = scrapy.Field()
    tax = scrapy.Field()
    price_without_tax = scrapy.Field()
    price_with_tax = scrapy.Field()
    number_of_reviews = scrapy.Field()
    InStock = scrapy.Field()
    num_of_items_available = scrapy.Field()
    current_price = scrapy.Field()
    date = scrapy.Field()