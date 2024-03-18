from immo_eliza.immo_eliza.items import ImmoElizaItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from utils.parse_data import parser
import json
import csv

class HousesSpider(CrawlSpider):
    name = "estate"
    allowed_domains = ["immoweb.be"]
    start_urls = [
        f"https://www.immoweb.be/fr/recherche/maison/a-vendre?countries=BE&page={x}&orderBy=newest"
        for x in range(1, 334)
    ]

    rules = (
        #Rule(LinkExtractor(allow=(r"page=",))),
        Rule(LinkExtractor(allow=(r"annonce",)), callback="parse_item"),
    )

    def parse_item(self, response):
        jscript = response.css("script[type='text/javascript']:contains('window.classified')::text").get()
        jscript = jscript.replace("window.classified = ", "").replace(";", "")
        jscript = json.loads(jscript)

        data = ImmoElizaItem()

        data["property_id"] = parser(jscript, ["id"], None)
        data["postal_code"] = parser(jscript, ["property", "location", "postalCode"], None)
        data["type_of_property"] = parser(jscript, ["property", "type"], None)
        data["subtype_of_property"] = parser(jscript, ["property", "subtype"], None)
        data["price"] = parser(jscript, ["price", "mainValue"], None)
        data["bedrooms"] = parser(jscript, ["property", "bedroomCount"], None)
        data["living_area"] = parser(jscript, ["property", "netHabitableSurface"], None)
        data["fireplace"] = parser(jscript, ["property", "fireplaceExists"], None)
        data["terrace"] = parser(jscript, ["property", "terraceSurface"], None)
        data["garden"] = parser(jscript, ["property", "fireplaceExists"], None)
        data["rooms"] = parser(jscript, ["property", "roomCount"], None)
        data["bathrooms"] = parser(jscript, ["property", "bathroomCount"], None)
        data["region"] = parser(jscript, ["property", "location", "region"], None)
        data["province"] = parser(jscript, ["property", "location", "province"], None)
        data["state_of_property"] = parser(jscript, ["property", "building", "condition"], None)
        data["facade_count"] = parser(jscript, ["property", "building", "facadeCount"], None)
        data["heating"] = parser(jscript, ["property", "energy", "heatingType"], None)
        data["kitchen"] = parser(jscript, ["property", "kitchen", "type"], None)
        data["furnished"] = parser(jscript, ["transaction", "sale", "isFurnished"], None)
        data["swimmingpool"] = parser(jscript, ["property", "hasSwimmingPool"], None)

        self.save_to_csv(data)

    def save_to_csv(self, data):
        # Specify the CSV filename and fieldnames
        filename = "datasets/houses/houses_data.csv"
        fieldnames = ["property_id", "postal_code", "type_of_property", "subtype_of_property", "price", "bedrooms", "living_area", "openfire", "terrace", "garden",
            "rooms", "bathrooms", "region", "province", "state_of_property", "facade_count", "heating", "kitchen", "furnished", "swimmingpool"]

        # Open the CSV file in write mode
        with open(filename, "a", newline="") as csvfile:
            # Create a CSV writer object
            csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the header if the file is empty
            if csvfile.tell() == 0:
                csv_writer.writeheader()

            # Write the data to the CSV file
            csv_writer.writerow({
                "property_id": data["property_id"],
                "postal_code": data["postal_code"],
                "type_of_property": data["type_of_property"],
                "subtype_of_property": data["subtype_of_property"],
                "price": data["price"],
                "bedrooms": data["bedrooms"],
                "living_area": data["living_area"],
                "openfire": data["fireplace"],
                "terrace": data["terrace"],
                "garden": data["garden"],
                "rooms":data["rooms"],
                "bathrooms":data["bathrooms"],
                "region":data["region"],
                "province":data["province"],
                "state_of_property":data["state_of_property"],
                "facade_count":data["facade_count"],
                "heating":data["heating"],
                "kitchen":data["kitchen"],
                "furnished":data["furnished"],
                "swimmingpool":data["swimmingpool"],
            })
        self.log(f"Saved data to {filename}")
