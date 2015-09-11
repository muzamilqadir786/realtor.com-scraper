# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RealtorItem(scrapy.Item):
    # define the fields for your item here like:
    Name = scrapy.Field()
    URL = scrapy.Field()
    Designation = scrapy.Field()
    Brokerage = scrapy.Field()
    Phone = scrapy.Field()
    Location = scrapy.Field()
    Address = scrapy.Field()
    Website = scrapy.Field()
    Facebook = scrapy.Field()
    LinkedIn = scrapy.Field()
    profilePhone = scrapy.Field()

