import os
import requests
import xmltodict
import csv


class API:
                        # new name for the variable API_DATA
    def __init__(self, API_DATA):

        # TODO: Needs to be more dynamic to be able to use different types of login credentials i.e OAuth
        self.auth.username(os.environ[API_DATA['credentials']['user']])
        self.auth.password(os.environ[API_DATA['credentials']['password']])

        # TODO: Dynamically allow endpoints i.e vehicle, brand etc
        self.auth.URL = API_DATA['ENDPOINT']

        # SET API URL


        response = requests.get(self.auth.url, auth=(self.auth.username, self.auth.password))

        xmltodict.parse(response.text)


        api_url_stations = 'http://webservices.ns.nl/ns-api-stations-v2'
        rs = requests.get(api_url_stations, auth=auth_details)
        alle_stations = xmltodict.parse(rs.text)




        # TODO: Function that gets data based on the inserted datatype and protocol set i.e number plate