# standard library imports
import requests
import json
import os

# custom library imports
from car import Car


# TODO: PRETTY UP THE ENTIRE FILE
# TODO: Can be made more global but for testing purposes static has been chosen.
class RDWAPI:
    # Overview
    # TODO: Function that gets record based on URL i.e def get_data_by_query(query)
    """
    Init creates an object based on the API data, the get car function only neeeds an number plate and will return a car object
    """


    # Setting up the basic configuration for APIs, for the scope of this project (as of 6th of November 2017) the only planned API found at https://overheid.io/documentatie/voertuiggegevens
    def __init__(self, number_plate = None):
        # TODO: Needs to be more dynamic to be able to use different types of login credentials i.e OAuth
        # Using authentication from OS rather than key to prevent collisions and license revokes due to public publication
        # self.auth = {'app_token': os.environ['OPEN_DATA-KEY'], 'hash': os.environ['OPEN_DATA-HASH']}

        # TODO: Dynamically allow endpoints i.e vehicle, brand etc
        self.url = 'https://opendata.rdw.nl/resource/m9d7-ebf2.json?'
        self.separator = '?'
        self.AppToken = '8Bb5z94nzesdifgi8O7aHqAK2'
        self.AppPretense = "$$app_token="
        self.urlTypeSeperator = '&'
        self.number_plate_query_var = 'kenteken='

        if number_plate is not None:
            self.number_plate = number_plate

    """
    Currently there isn't one dataset with all the information we want which is 
        1.The first time it was assigned in the netherlands
        2.The fuel type i.e Gas, Diesel, Electric etc
    """

    # TODO: Function that gets data based on the inserted data type and protocol set i.e number plate
    def get_car(self, number_plate):
        if number_plate is None:
            raise ValueError('Number plate is unknown /= None')
        query = number_plate

        APIquery = self.separator + self.number_plate_query_var + query

        # finally sending out to the overheid.io API access point
        #response = requests.get(self.url + APIquery)
        #if self.AppToken is not None:

        print(self.url + self.AppPretense + self.AppToken + self.urlTypeSeperator + APIquery)
        response = requests.get(self.url + self.AppPretense + self.AppToken + self.urlTypeSeperator + APIquery)

        # If status code is 200, the appropriate range has been selected so no issues SHOULD emerge
        if response.status_code == 200:
            # Because the DICT is inside a LIST an extract is placed
            # TODO: TRY-CATCH
            car_data = json.loads(response.text)[0]

            # second api call to get the fuel type
            response = requests.get(car_data['api_gekentekende_voertuigen_brandstof'] + APIquery)
            if response.status_code == 200:
                # TODO: Try-CATCH
                fuel = json.loads(response.text)[0]

                car_data.update(fuel)
                # TODO: WAAY more fail safes and exceptions placed
                return Car(**car_data)

            else:
                raise Exception(
                    'Invalid status code, response is not as expected, response code: ' + str(response.status_code))

        else:
            raise Exception('Invalid status code, response is not as expected, response code: ' + str(response.status_code))


cr = RDWAPI()
print(cr.get_car('24PGRL'))
