"""
--scrapper_lambda.py--
An AWS lambda function for web scrapping vehicle data.
Needs the Scrapper class from scrapper.py
"""
import os
import sys
import csv
import json
import boto3
import argparse

from datetime import datetime
from scrapper import Scrapper

NUM_OF_PAGES = 10
DESTINATION_BUCKET = "used-car-listing-prices"
DIR_NAME = os.path.dirname(__file__)


def load_scrapping_links(vehicle_category):
    """
    """
    vehicles = []
    with open(f"{DIR_NAME}/vehicles.json") as fhandle:
        vehicles_dict = json.load(fhandle)
    for vehicle_brand in vehicles_dict:
        make = vehicle_brand.get("make")
        target_vehicle = list(
            filter(lambda x: x.get("type") == vehicle_category,
                   vehicle_brand.get("vehicles")))
        if target_vehicle:
            target_vehicle = target_vehicle[0]
            model = target_vehicle.get("model")
            urls = target_vehicle.get("base_url")
            vehicles.append((make, model, urls))
    return vehicles


def write(file_handler, records, header=None):
    csv_writer = csv.writer(file_handler,
                            delimiter=',',
                            quotechar='"',
                            quoting=csv.QUOTE_MINIMAL)
    if header:
        csv_writer.writerow(header)
    csv_writer.writerows(records)


def create_directory(name):
    """
    Create a directory at the same level as this module.
    """
    path = os.path.join(DIR_NAME, name)
    try:
        os.mkdir(path)
    except FileExistsError:
        pass


def scrap_and_upload(vehicle_category):
    """
    """
    if vehicle_category is None:
        sys.exit("vehicle category cannot be null")
    vehicles = load_scrapping_links(vehicle_category)

    start_time = datetime.utcnow().strftime("%Y-%m-%d")
    create_directory(f"tmp")
    create_directory(f"tmp/{vehicle_category}")
    file_path = f"{DIR_NAME}/tmp/{vehicle_category}/{start_time}.csv"

    if os.path.exists(file_path):
        header = None
    else:
        header = ["Make", "Model", "Trim", "Year", "Mileage", "Price"]

    for make, model, urls in vehicles:
        for website_name, link in urls.items():
            if website_name == 'cg':
                urlsuffix = "#resultsPage="
            elif website_name == 'ed':
                urlsuffix = "?pagenumber="
            site_scrapper = Scrapper(website_name, link, urlsuffix, make,
                                     model, vehicle_category)
            site_scrapper.fetch_batch(NUM_OF_PAGES)
            if site_scrapper.listings:
                with open(file_path, "a") as csvfile:
                    write(csvfile, site_scrapper.listings, header)
                    header = None

    if os.path.exists(file_path):
        s3_client = boto3.client('s3')
        s3_client.upload_file(file_path, DESTINATION_BUCKET,
                              f"{vehicle_category}/{start_time}.csv")


if __name__ == "__main__":
    import time
    categories = [
        "compact-sedan", "mid-size-sedan", "full-size-sedan", "compact-suv",
        "mid-size-suv", "full-size-suv", "all"
    ]
    parser = argparse.ArgumentParser()
    parser.add_argument("-c",
                        "--category",
                        help="Vehicle category, e.g. mid-size-sedan",
                        default="all")
    args = parser.parse_args()

    if args.category not in categories:
        sys.exit("Invalid category")
    if args.category == "all":
        for category in categories[:-1]:
            scrap_and_upload(category)
            time.sleep(30)
    else:
        scrap_and_upload(args.category)
