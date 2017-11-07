import os
import requests
import ssl
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
import json
import csv
import PSdebug
import config



class API:
    # Overview
    # TODO: Function that gets record based on URL i.e def get_data_by_query(query)

    # Setting up the basic configuration for APIs, for the scope of this project (as of 6th of November 2017) the only planned API found at https://overheid.io/documentatie/voertuiggegevens
    def __init__(self, TYPE):


        # TODO: Needs to be more dynamic to be able to use different types of login credentials i.e OAuth
        self.auth = ()

        # TODO: Dynamically allow endpoints i.e vehicle, brand etc
        self.url = 'https://overheid.io/api/voertuiggegevens/'

        # TODO: Future proofing for multiple end points API
        self.type = TYPE



        # TODO: Function that gets data based on the inserted datatype and protocol set i.e number plate

    def get_by_query(self):
        auth_details = (os.environ['RDW-KEY'])

        response = requests.get("https://overheid.io/api/voertuiggegevens/", auth=auth_details)
        print(response)

ao = API('RDW')
print(ao.get_by_query())