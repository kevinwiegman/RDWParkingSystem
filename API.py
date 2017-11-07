import os
import requests
import ssl
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
import json
import csv
import PSdebug
import config
from car import Car


# TODO: Can be made more global but for testing purposes static has been chosen.
class RDWAPI:
    # Overview
    # TODO: Function that gets record based on URL i.e def get_data_by_query(query)

    # Setting up the basic configuration for APIs, for the scope of this project (as of 6th of November 2017) the only planned API found at https://overheid.io/documentatie/voertuiggegevens
    def __init__(self, TYPE):
        # TODO: Needs to be more dynamic to be able to use different types of login credentials i.e OAuth
        # Using authentication from OS rather than key to prevent collisions and license revokes due to public publication
        self.auth = os.environ['RDW-KEY']

        # TODO: Dynamically allow endpoints i.e vehicle, brand etc
        self.url = 'https://overheid.io/api/voertuiggegevens/'

        # TODO: Future proofing for multiple end points API
        self.type = TYPE



        # TODO: Function that gets data based on the inserted datatype and protocol set i.e number plate

    def get_car(self, number_plate):
        if number_plate is None:
            raise ValueError('Number plate is unknown /= None')
        query = number_plate

        baseURL = 'https://overheid.io/api/voertuiggegevens/'
        APIurl = baseURL.join(query)

        # finally sending out to the overheid.io API access point
        response = requests.get(APIurl, self.auth)

        # TODO: RESPONSE NEEDS TO BE CLEANSED
        print(response)



    """
    Currently there isn't one dataset with all the information we want which is 
        1.The first time it was assigned in the netherlands
        2.The fuel type i.e Gas, Diesel, Electric etc
    """