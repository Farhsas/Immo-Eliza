# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import psycopg2


class ImmoElizaPipeline:
    def __init__(self) -> None:
        try:
            hostname = "localhost"
            username = "postgres"
            password = "postgres"
            database = "immo-eliza"

            self.connection = psycopg2.connect(host=hostname, user=username, password=password, database=database)
            self.cur = self.connection.cursor()
        except psycopg2.OperationalError as er:
            print(f"Error connecting to the database: {er}")

    def open_crawler(self, crawler):
        try:
            self.cur.execute(
                """
                CREATE TABLE IF NOT EXISTS sales(
                    property_id INT PRIMARY KEY,
                    postal_code INT,
                    type_of_property VARCHAR(255),
                    subtype_of_property VARCHAR(255),
                    price INT,
                    bedrooms INT,
                    living_area INT,
                    openfire BOOLEAN,
                    terrace INT,
                    garden INT,
                    rooms INT,
                    bathrooms INT,
                    region VARCHAR(255),
                    province VARCHAR(255),
                    state_of_property VARCHAR(255),
                    facade_count INT,
                    heating VARCHAR(255),
                    kitchen VARHCAR(255),
                    furnished BOOLEAN,
                    swimmingpool BOOLEAN,
                )
                """
            )
        except psycopg2.Error as er:
            crawler.logger.error(f"Error creating table: {er}")

    def process_item(self, item, crawler):
        self.cur.execute(
            "SELECT * FROM sales WHERE property_id = %s", (item["property_id"],)
        )
        result = self.cur.fetchone()

        if result:
            crawler.logger.warn("Item already in database: %s" % item["property_id"])

        elif item["price"] is None:
            crawler.logger.warn("Item has no price!")

        else:
            self.cur.execute(
                """
                INSERT INTO sales(
                    property_id,
                    postal_code,
                    type_of_property,
                    subtype_of_property,
                    price,
                    bedrooms,
                    living_area,
                    openfire,
                    terrace,
                    garden,
                    rooms,
                    bathrooms,
                    region,
                    province,
                    state_of_property,
                    facade_count,
                    heating,
                    kitchen,
                    furnished,
                    swimmingpool,
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                )
                """,
                (
                    item["property_id"],
                    item["postal_code"],
                    item["type_of_property"],
                    item["subtype_of_property"],
                    item["price"],
                    item["bedrooms"],
                    item["living_area"],
                    item["openfire"],
                    item["terrace"],
                    item["garden"],
                    item["rooms"],
                    item["bathrooms"],
                    item["region"],
                    item["province"],
                    item["state_of_property"],
                    item["facade_coutn"],
                    item["heating"],
                    item["kitchen"],
                    item["furnished"],
                    item["swimmingpool"]
                ),
            )

            self.connection.commit()
        return item


    def close_crawler(self, crawler):
        try:
            self.cur.close()
            self.connection.close()
        except psycopg2.Error as er:
            crawler.logger.error(f"Error closing the database connection= {er}")
