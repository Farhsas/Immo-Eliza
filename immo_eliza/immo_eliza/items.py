# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class ImmoElizaItem(Item):
    property_id = Field()
    region = Field()
    province = Field()
    postal_code = Field()
    type_of_property = Field()
    subtype_of_property = Field()
    living_area = Field()
    rooms = Field()
    bedrooms = Field()
    bathrooms = Field()
    state_of_property = Field()
    facade_count = Field()
    heating = Field()
    kitchen = Field()
    garden = Field()
    terrace = Field()
    fireplace = Field()
    furnished = Field()
    swimmingpool = Field()
    price = Field()
