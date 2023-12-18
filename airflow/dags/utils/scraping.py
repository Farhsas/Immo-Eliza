import httpx  # Used to make asynchronous HTTP requests
import asyncio  # Used for handling asynchronous tasks and event loops
import json  # Used to work with JSON data (parsing and serialization)
import pandas as pd  # Used for data manipulation
import time
import ssl  # Used to handle Secure Sockets Layer (SSL) errors and configurations
from bs4 import BeautifulSoup  # Used for web scraping and parsing HTML content
from itertools import chain  # Used for chaining together iterable items or element


def property_id(script):
    """
    Extracts the property ID from a script dictionary.

    Args:
        script (dict): The script dictionary containing property information.

    Returns:
        str: The property ID or None if not found.
    """
    good_dict = script
    try:
        return good_dict["id"]
    except:
        return None


def locality_name(script):
    """
    Extracts the locality name from a script dictionary.

    Args:
        script (dict): The script dictionary containing property information.

    Returns:
        str: The locality name or None if not found.
    """
    good_dict = script
    try:
        return good_dict["property"]["location"]["locality"]
    except:
        return None


def postal_code(script):
    """
    Extracts the postal code from a script dictionary.

    Args:
        script (dict): The script dictionary containing property information.

    Returns:
        str: The postal code or None if not found.
    """
    good_dict = script
    try:
        return good_dict["property"]["location"]["postalCode"]
    except:
        return None


def type_of_property(script):
    """
    Extracts the property ID from a script dictionary.

    Args:
        script (dict): The script dictionary containing property information.

    Returns:
        str: The property ID or None if not found.
    """
    good_dict = script
    try:
        return good_dict["property"]["type"]
    except:
        return None


def subtype_of_property(script):
    """
    Extracts the subtype_of_property from a script dictionary.

    Args:
        script (dict): The script dictionary containing property information.

    Returns:
        str: The subetype_of_property or None if not found.
    """
    good_dict = script
    try:
        return good_dict["property"]["subtype"]
    except:
        return None


def price(script):
    """
    Extracts the price from a script dictionary.

    Args:
        script (dict): The script dictionary containing property information.

    Returns:
        str: The price or None if not found.
    """
    good_dict = script
    try:
        return good_dict["transaction"]["sale"]["price"]
    except:
        return None


def type_of_sale(script):
    """
    Extracts the type_of_sale from a script dictionary.

    Args:
        script (dict): The script dictionary containing property information.

    Returns:
        str: the type_of_sale or None if not found.
    """
    good_dict = script
    try:
        if good_dict["flags"]["isPublicSale"]:
            return "PublicSale"
        elif good_dict["flags"]["isNewlyBuilt"]:
            return "NewlyBuilt"
        elif good_dict["flags"]["isNotarySale"]:
            return "NotarySale"
        elif good_dict["flags"]["isAnInteractiveSale"]:
            return "InteractiveSale"
        elif good_dict["flags"]["isUnderOption"]:
            return "UnderOption"
        else:
            return None
    except:
        return None


def number_of_rooms(script):
    """
    Extracts the number_of_rooms from a script dictionary.

    Args:
        script (dict): The script dictionary containing property information.

    Returns:
        str: The number_of_rooms or None if not found.
    """
    good_dict = script
    try:
        return good_dict["property"]["bedroomCount"]
    except:
        return None


def living_area(script):
    """
    Extracts the living_area from a script dictionary.

    Args:
        script (dict): The script dictionary containing property information.

    Returns:
        str: The living_are or None if not found.
    """
    good_dict = script
    try:
        return good_dict["property"]["netHabitableSurface"]
    except:
        return None


def equipped_kitchen(script):
    """
    Extracts the equipped_kitchen from a script dictionary.

    Args:
        script (dict): The script dictionary containing property information.

    Returns:
        str: 1 if equipped, 0 if not equipped or None if not found.
    """
    good_dict = script
    try:
        if good_dict["property"]["kitchen"]["type"]:
            return 1
        else:
            return 0
    except:
        return None


def furnished(script):
    """
    Extracts the furnished from a script dictionary.

    Args:
        script (dict): The script dictionary containing property information.

    Returns:
        str: 1 if furnished, O if not furnished or None if not found.
    """
    good_dict = script
    try:
        if good_dict["transaction"]["sale"]["isFurnished"]:
            return 1
        else:
            return 0
    except:
        return None


def open_fire(script):
    """
    Extracts the open_fire from a script dictionary.

    Args:
        script (dict): The script dictionary containing property information.

    Returns:
        str: 1 if there is a fire place, 0 if there isn't one or None if not found.
    """
    good_dict = script
    try:
        if good_dict["property"]["fireplaceExists"]:
            return 1
        else:
            return 0
    except:
        return None


def terrace(script):
    """
    Extracts the terrace from a script dictionary.

    Args:
        script (dict): The script dictionary containing property information.

    Returns:
        str: the surface of the terrace if there is one, 0 if there is no terrace or None if not found.
    """
    good_dict = script
    try:
        if good_dict["property"]["hasTerrace"]:
            return good_dict["property"]["terraceSurface"]
        else:
            return 0
    except:
        return 0


def garden(script):
    """
    Extracts the garden from a script dictionary.

    Args:
        script (dict): The script dictionary containing property information.

    Returns:
        str: the garden surface if there is one, 0 if there is no garden or None if not found.
    """
    good_dict = script
    try:
        if good_dict["property"]["hasGarden"]:
            return good_dict["property"]["gardenSurface"]
        else:
            return 0
    except:
        return 0


def surface_of_good(script):
    """
    Extracts the surface_of_good from a script dictionary.

    Args:
        script (dict): The script dictionary containing property information.

    Returns:
        str: The surface_of_good or None if not found.
    """
    good_dict = script
    try:
        return good_dict["property"]["land"]["surface"]
    except:
        return None


def number_of_facades(script):
    """
    Extracts the number_of_facades from a script dictionary.

    Args:
        script (dict): The script dictionary containing property information.

    Returns:
        str: The number_of_facades or None if not found.
    """
    good_dict = script
    try:
        return good_dict["property"]["building"]["facadeCount"]
    except:
        return None


def swimming_pool(script):
    """
    Extracts the sswimming_pool from a script dictionary.

    Args:
        script (dict): The script dictionary containing property information.

    Returns:
        str: True if there is one, False if not or False if not found.
    """
    good_dict = script
    try:
        if good_dict["property"]["hasSwimmingPool"]:
            return True
        else:
            return False
    except:
        return False


def state_of_building(script):
    """
    Extracts the state_of_building from a script dictionary.

    Args:
        script (dict): The script dictionary containing property information.

    Returns:
        str: The state_of_building or None if not found.
    """
    good_dict = script
    try:
        return good_dict["property"]["building"]["condition"]
    except:
        return None


async def fetch_links(url, client):
    """
    Fetches and extracts property links from a given URL.

    Args:
        url (str): The URL to fetch property links from.
        client (httpx.AsyncClient): An HTTP client for making asynchronous requests.

    Returns:
        list of str: A list of property links or an empty list if an error occurs.
    """
    try:
        links = []
        r = await client.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        for tag in soup.find_all("a", {"class": "card__title-link"}):
            links.append(tag.get("href"))

        return links

    except httpx.ConnectError as ce:
        print(f"Connection error: {ce}")
    except httpx.HTTPStatusError as hse:
        print(f"HTTP status error: {hse}")
    except ssl.SSLSyscallError as ssl_error:
        print(f"SSL error: {ssl_error}")
    except ssl.SSLWantReadError as ssl_error:
        print(f"SSL read error: {ssl_error}")
    except ssl.SSLError as ssl_error:
        print(f"SSL error: {ssl_error}")
    except Exception as e:
        print(f"An error occurred: {e}")


async def get_links_houses():
    """
    Asynchronously fetches property listing links from multiple pages of a real estate website.

    This function uses an asynchronous HTTP client to retrieve property listing links from multiple
    pages of a real estate website, specifically from the immoweb.be website. It generates a list of
    asynchronous tasks to fetch links from different pages and then gathers the results.

    Returns:
        List[str]: A list of property listing links as strings.

    Note:
        This function is specifically designed for the immoweb.be website and may not work for
        other websites without appropriate modifications to the URL format.
    """
    async with httpx.AsyncClient(timeout=None) as client:
        tasks = []
        for i in range(1, 334):
            url = f"https://www.immoweb.be/en/search/house/for-sale?countries=BE&page={i}&orderBy=newest"
            tasks.append(asyncio.ensure_future(fetch_links(url, client)))
        return await asyncio.gather(*tasks)


async def get_links_apartments():
    """
    Asynchronously fetches property listing links from multiple pages of a real estate website.

    This function uses an asynchronous HTTP client to retrieve property listing links from multiple
    pages of a real estate website, specifically from the immoweb.be website. It generates a list of
    asynchronous tasks to fetch links from different pages and then gathers the results.

    Returns:
        List[str]: A list of property listing links as strings.

    Note:
        This function is specifically designed for the immoweb.be website and may not work for
        other websites without appropriate modifications to the URL format.
    """
    async with httpx.AsyncClient(timeout=None) as client:
        tasks = []
        for i in range(1, 334):
            url = f"https://www.immoweb.be/en/search/apartment/for-sale?countries=BE&page={i}&orderBy=newest"
            tasks.append(asyncio.ensure_future(fetch_links(url, client)))
        return await asyncio.gather(*tasks)


async def get_script(url, client):
    """
    Asynchronously fetches and parses JavaScript script data from a web page.

    This function uses an asynchronous HTTP client to fetch the content of a specified URL and
    extracts JavaScript script data from the HTML page. It then parses and converts the script
    data into a Python dictionary, assuming the script contains a valid JSON structure.

    Args:
        url (str): The URL of the web page containing JavaScript script data.
        client (httpx.AsyncClient): An HTTP client for making asynchronous requests.

    Returns:
        dict: A dictionary containing data extracted from the JavaScript script.
              Returns None if an error occurs during data extraction or parsing.

    Note:
        This function assumes that the JavaScript script on the web page contains a JSON structure
        that can be successfully parsed. If the script structure is not as expected, it may return
        None.

    Example:
        The function can be used to extract structured data from web pages for further processing
        or analysis, such as property information in real estate listings.
    """
    r = await client.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    try:
        body = soup.find("body")
        script = body.find("script", {"type": "text/javascript"})

        house_data = script.string
        house_data.strip()

        window_classified = house_data[house_data.find("{") : house_data.rfind("}") + 1]

        good_dict = json.loads(window_classified)

        return good_dict
    except:
        return None


async def get_details(urls):
    """
    Asynchronously fetches and extracts property details from a list of URLs.

    This function utilizes an asynchronous HTTP client to fetch property details from a list of
    URLs. It creates a list of asynchronous tasks for each URL and then gathers the results into
    a collection of property details, represented as dictionaries.

    Args:
        urls (List[str]): A list of URLs from which property details are to be extracted.

    Returns:
        List[dict]: A list of dictionaries, each containing property details.
                    Returns an empty list if an error occurs during data extraction.

    Example:
        The function is typically used to extract structured property details, such as price,
        location, and features, from real estate listings on a website for further analysis or
        storage in a structured format, like a database or CSV file.
    """
    limits = httpx.Limits(max_connections=25)
    async with httpx.AsyncClient(timeout=None, limits=limits) as client:
        tasks = []
        for url in urls:
            tasks.append(asyncio.ensure_future(get_async_detail(url, client)))
        return await asyncio.gather(*tasks)


async def get_async_detail(url, client):
    """
    Extracts property details from a given URL.

    Args:
        url (str): The URL to fetch property details from.
        client (httpx.AsyncClient): An HTTP client for making asynchronous requests.

    Returns:
        dict: A dictionary containing property details.
    """
    script = await get_script(url, client)
    data = {
        "PropertyID": property_id(script),
        "LocalityName": locality_name(script),
        "PostalCode": postal_code(script),
        "TypeOfProperty": type_of_property(script),
        "SubtypeOfProperty": subtype_of_property(script),
        "Price": price(script),
        "TypeOfSale": type_of_sale(script),
        "NumberOfRooms": number_of_rooms(script),
        "LivingArea": living_area(script),
        "EquippedKitchen": equipped_kitchen(script),
        "Furnished": furnished(script),
        "OpenFire": open_fire(script),
        "Terrace": terrace(script),
        "Garden": garden(script),
        "Surface": surface_of_good(script),
        "NumberOfFacades": number_of_facades(script),
        "SwimmingPool": swimming_pool(script),
        "StateOfBuilding": state_of_building(script),
    }
    print(data)
    return data


def houses_scraper():
    """
    The main function that orchestrates the data extraction process and saves the data to a CSV file.
    """
    links = asyncio.run(get_links_houses())
    detail_links = []
    for link in chain(links):
        for l in chain(link):
            detail_links.append(l)

    details = asyncio.run(get_details(detail_links))

    df = pd.DataFrame(details)
    df.to_csv("airflow/dags/datasets/houses_data.csv")


def apartments_scraper():
    """
    The main function that orchestrates the data extraction process and saves the data to a CSV file.
    """
    links = asyncio.run(get_links_apartments())
    detail_links = []
    for link in chain(links):
        for l in chain(link):
            detail_links.append(l)

    details = asyncio.run(get_details(detail_links))

    df = pd.DataFrame(details)
    df.to_csv("airflow/dags/datasets/apartments_data.csv")


if __name__ == "__main__":
    start_time = time.time()
    houses_scraper()
    apartments_scraper()
    print("--- %s seconds ---" % (time.time() - start_time))
