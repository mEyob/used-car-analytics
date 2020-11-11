"""
--scrapper_lambda.py--
An AWS lambda function for web scrapping vehicle data.
Needs the Scrapper class from scrapper.py
"""
import sys
import csv
import json
import boto3
from datetime import datetime
from scrapper import Scrapper

NUM_OF_PAGES = 10
DESTINATION_BUCKET = "used-car-prices"


def load_scrapping_links(vehicle_category):
    """
    """
    vehicles = []
    with open("vehicles.json") as fhandle:
        vehicles_dict = json.load(fhandle)
    for vehicle_brand in vehicles_dict:
        make = vehicle_brand.get("make")
        target_vehicle = filter(lambda x: x.get("type") == vehicle_category,
                                vehicle_brand.get("vehicles"))
        target_vehicle = list(target_vehicle)[0]
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


def lambda_handler(event, context):
    """
    """
    vehicle_category = event.get("vehicle_category")
    if vehicle_category is None:
        sys.exit("vehicle category cannot be null")

    vehicles = load_scrapping_links(vehicle_category)
    header = ["Make", "Model", "Trim", "Year", "Mileage", "Price"]
    start_time = datetime.utcnow().strftime("%Y-%m-%d")
    for make, model, urls in vehicles:
        for website_name, link in urls.items():
            if website_name == 'cg':
                urlsuffix = "#resultsPage="
            site_scrapper = Scrapper(website_name, link, urlsuffix, make,
                                     model, vehicle_category)
            site_scrapper.fetch_batch(NUM_OF_PAGES)
            if site_scrapper.listings:
                with open(f"/tmp/{start_time}.csv", "a") as csvfile:
                    write(csvfile, site_scrapper.listings, header)
                    header = None

    s3_client = boto3.client('s3')
    s3_client.upload_file(f"/tmp/{start_time}.csv", DESTINATION_BUCKET,
                          f"{vehicle_category}/{start_time}.csv")
