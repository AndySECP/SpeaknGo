import herepy
import yaml
import requests
import json
import numpy as np

class RouteComputer:
    def __init__(self):
        #Getting the API config

        with open("mobility_options_queries/config.yml", 'r') as stream:
            try:
                cfg = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)


        self.HERE_ID = cfg["here_api"]["here_id"]
        self.HERE_PASSWD = cfg["here_api"]["here_passwd"]

    def computeLatLonFromAdress(self, adress):
        """
        TODO
        """
        geocoderApi = herepy.GeocoderApi(self.HERE_ID, self.HERE_PASSWD)

        pos_geocoder = geocoderApi.free_form(adress)
        pos_dict = pos_geocoder.as_dict()['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]
        pos = [pos_dict['Latitude'], pos_dict['Longitude']]

        return pos

    def getOption(self, start_pos, end_pos, time, transportation_type):
        """Returns the characteristics dictionary for a trip from start_pos to end_pos with the chosen transportation type

        Parameters
        ----------
        start_pos : Array [Longitude, Latitude]
            Starting point
        end_pos : Array [Longitude, Latitude]
            Ending point
        time : Structured as '2019-07-20T12:00:00'
            Starting time
        transportation_type : String
            So far, must be "car", "pedestrian" or "public transport"

        Returns
        -------
        Dictionary
            A dictionary of the characteristics:
            Distance (in meters), time (in seconds), type (car, pedestrian, public transport), price ($)
        """

        routingPublicTransportApi = herepy.public_transit_api.PublicTransitApi(self.HERE_ID, self.HERE_PASSWD)
        routingApi = herepy.routing_api.RoutingApi(self.HERE_ID, self.HERE_PASSWD)

        characteristics = dict()

        if transportation_type.lower() == "car":
            response = routingApi.car_route(start_pos, end_pos)
            characteristics['type'] = "car"
            characteristics['distance'] = int(response.as_dict()['response']['route'][0]['summary']['distance'] / 1609) # in miles
            characteristics['time'] = int(response.as_dict()['response']['route'][0]['summary']['baseTime'] / 60) # in minutes
            characteristics['price'] = 0.80 + 0.21*characteristics['time'] + 1.10*characteristics['distance']
        elif transportation_type.lower() == "pedestrian":
            response = routingApi.pedastrian_route(start_pos, end_pos)
            characteristics['type'] = "pedestrian"
            characteristics['price'] = 0
        elif transportation_type.lower() == "public transport":
            response = routingApi.public_transport(start_pos, end_pos, False)

            print(response)

            characteristics['type'] = "public transport"

            route_public_transport = routingPublicTransportApi.calculate_route(start_pos, end_pos, time)

            list_of_fares = route_public_transport.as_dict()['Res']['Connections']['Connection'][0]['Tariff']['Fares'][0]['Fare']
            pricePublicTransport = 0

            for fare_obj in list_of_fares:
                pricePublicTransport += fare_obj['price']

            characteristics['price'] = pricePublicTransport
        else:
            raise NotImplementedError

        characteristics['distance'] = int(response.as_dict()['response']['route'][0]['summary']['distance'] / 1609) # in miles
        characteristics['time'] = int(response.as_dict()['response']['route'][0]['summary']['baseTime'] / 60) # in minutes

        return characteristics


    # option_list is a list of dictionaries
    def displayOptions(self, option_list):
        """
        Parameters
        ----------
        option_list : List of route characteristics dictionary
        """
        for option in option_list:
            print('{0}: Distance (km): {1:.2f}, Time (min): {2:.2f}, Cost($): {3:.2f}'.format(option['type'], option['distance']/1000, option['time']/60, option['price']))


    def getClosestInterest(self, position=[37.7874,-122.3964], type='supermarket'):
        """Given a position and a certain type of interest, returns the closest one of the type.

        Parameters
        ----------
        position : list of coordonates, [Longitude, Latitude]
        type : str, optional
            Type of interest, by default 'supermarket'

        Returns
        -------
        Place returned by API, dictionary-like
        """
        placesResponse = placesApi.nearby_places(position)
        placesResponse = placesApi.onebox_search(position, type)

        places = placesResponse.as_dict()['results']['items']
        closest_place = None
        distance_closest = np.inf
        for place in places:
            # ['position', 'distance', 'title', 'averageRating', 'category', 'icon', 'vicinity', 'having', 'type', 'href', 'id']
            #print(place['title'], place['distance'])
            if place['distance'] < distance_closest:
                closest_place = place
                distance_closest = place['distance']

        return closest_place
