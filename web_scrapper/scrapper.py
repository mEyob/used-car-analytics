"""
--scrapper.py--
Module for scrapping and parsing used car data
"""
import os
import time
import random
import logging
import requests
from datetime import datetime
from bs4 import BeautifulSoup

log_dir = os.path.join(os.path.dirname(__file__), os.pardir, "log")
try:
    os.mkdir(log_dir)
except FileExistsError:
    pass

logging.basicConfig(level=logging.INFO,
                    filename=os.path.join(
                        log_dir,
                        datetime.now().strftime("%y-%m-%d") + ".log"),
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%y-%m-%d %H:%M:%S')


class Scrapper():
    def __init__(self, website_name, base_url, page_sufix, make, model,
                 category):
        """
        """
        self.website_name = website_name
        self.base_url = base_url
        self.page_sufix = page_sufix
        self.make = make
        self.model = model
        self.category = category
        self.listings = []

    def fetch(self, url):
        """
        Fetch a single page of listings
        """
        headers = {
            'authority': 'scrapeme.live',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        try:
            response = requests.get(url, headers=headers, timeout=5)
        except:
            response = None
        return response

    def fetch_batch(self, total_pages):
        """
        Fetch all pages for a specific Make & Model
        """
        pages_fetched = 0

        # Randomize the sequence of pages being fetched to
        # reduce the chance of being labelled as robot
        pages = [1]
        pages.extend(random.sample(range(2, total_pages + 1), total_pages - 1))
        start_time = time.time()

        for page_num in pages:
            url = self.base_url + self.page_sufix + str(page_num)
            response = self.fetch(url)

            # To reduce the chance of being labeled as robot,
            # wait for a few seconds before fetching the next page
            # random_seconds = 5 * random.random()
            # time.sleep(random_seconds)

            if response and response.status_code == 200:
                pages_fetched += 1
                self.parse(response.text)
        end_time = time.time()
        vehicles_parsed = len(self.listings)

        time_stat = f"total time {end_time - start_time} seconds"
        message = f"Website {self.website_name.upper()}: total pages fetched {pages_fetched} : {vehicles_parsed} {self.make} {self.model} vehicles parsed : {time_stat}"
        logging.info(message)

    def parse(self, raw_html):
        """
        Parse vehicle(s) information from html page
        """
        bs_object = BeautifulSoup(raw_html, "html.parser")

        if self.website_name == "cg":
            parser = self.cg_parser
        elif self.website_name == "ed":
            parser = self.ed_parser
        try:
            parser(bs_object)
        except:
            pass

    def cg_parser(self, bs_object):
        """
        """
        for listing in bs_object.find_all("div", class_="bladeWrap"):
            header = listing.find("h4").text.strip()
            popover = listing.find(
                "div",
                "popoverWrapper listingDetailsPopover_wrapper").text.strip()
            header = header.replace(popover, "").strip()
            year, make, model, *trim = header.split()
            trim = " ".join(trim)

            price = listing.find("span", class_="price").text.strip()
            price = price.replace("$", "").replace(",", "")

            mileage = listing.find("p", class_="mileage").text.strip()
            mileage = mileage.replace(",", "").replace("mi", "").strip()

            self.listings.append([make, model, trim, year, mileage, price])

    def ed_parser(self, bs_object):
        """
        """
        for listing in bs_object.find_all(
                "div",
                class_="vehicle-info pl-1_25 pl-md-1 pl-lg-1_25 container-fluid"):
            price = listing.find(
                "span",
                class_="display-price font-weight-bold text-gray-darker"
            ).text.strip()
            price = price.replace("$", "").replace(",", "")

            header = listing.find(
                "h2",
                "card-title size-16 text-primary-darker font-weight-bold d-block mb-0_5"
            ).text.strip()
            header = header.strip("Certified ")
            year, make, model, *trim = header.split()
            if model.lower() != self.model.lower():
                continue
            trim = " ".join(trim)

            mileage = listing.find(["div", "span"],
                                   class_="size-14").text.strip()
            mileage = mileage.replace(",", "").replace("miles", "").strip()

            self.listings.append([make, model, trim, year, mileage, price])


if __name__ == "__main__":
    import csv
    import argparse

    # Command line arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("-u", "--url", help="URL of page to be scrapped")
    parser.add_argument("-w", "--source", help="Source website name")
    parser.add_argument("-s",
                        "--urlsuffix",
                        help="URL suffix",
                        default="#resultsPage=")
    parser.add_argument("-d",
                        "--vdetail",
                        help="Make, model and category of vehicle",
                        default="Toyota Camry ms")
    parser.add_argument("-p",
                        "--pages",
                        help="Number of pages to be scrapped",
                        type=int,
                        default=5)

    args = parser.parse_args()
    webscrapper = Scrapper(args.source, args.url, args.urlsuffix,
                           *args.vdetail.split())
    webscrapper.fetch_batch(args.pages)
    with open("listing.csv", "a") as file_handler:
        csv_writer = csv.writer(file_handler,
                                delimiter=',',
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(
            ["Make", "Model", "Trim", "Year", "Mileage", "Price"])
        csv_writer.writerows(webscrapper.listings)
