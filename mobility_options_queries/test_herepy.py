import herepy
import yaml
import requests
import json
import numpy as np


def getOption(start_pos, end_pos, time, transportation_type):
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

    characteristics = dict()

    if transportation_type.lower() == "car":
        response = routingApi.car_route(start_pos, end_pos)
        characteristics['type'] = "car"
        characteristics['distance'] = response.as_dict()['response']['route'][0]['summary']['distance'] # in meters
        characteristics['time'] = response.as_dict()['response']['route'][0]['summary']['baseTime'] # in seconds
        characteristics['price'] = 0.80 + 0.21*characteristics['time']/60 + 1.10*characteristics['distance']/1000/1.6
    elif transportation_type.lower() == "pedestrian":
        response = routingApi.pedastrian_route(start_pos, end_pos)
        characteristics['type'] = "pedestrian"
        characteristics['price'] = 0
    elif transportation_type.lower() == "public transport":
        response = routingApi.public_transport(start_pos, end_pos, False)
        characteristics['type'] = "public transport"

        route_public_transport = routingPublicTransportApi.calculate_route(start_pos, end_pos, time)

        list_of_fares = route_public_transport.as_dict()['Res']['Connections']['Connection'][0]['Tariff']['Fares'][0]['Fare']
        pricePublicTransport = 0

        for fare_obj in list_of_fares:
            pricePublicTransport += fare_obj['price']

        characteristics['price'] = pricePublicTransport
    else:
        raise NotImplementedError

    characteristics['distance'] = response.as_dict()['response']['route'][0]['summary']['distance'] # in meters
    characteristics['time'] = response.as_dict()['response']['route'][0]['summary']['baseTime'] # in seconds

    return characteristics


# option_list is a list of dictionaries
def displayOptions(option_list):
    """
    Parameters
    ----------
    option_list : List of route characteristics dictionary
    """
    for option in option_list:
        print('{0}: Distance (km): {1:.2f}, Time (min): {2:.2f}, Cost($): {3:.2f}'.format(option['type'], option['distance']/1000, option['time']/60, option['price']))


def getClosestInterest(position=[37.7874,-122.3964], type='supermarket'):
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

######

# PARAMS = {'app_id': HERE_ID,
#           'app_code': HERE_PASSWD,
#           'at': "37.7874,-122.39638",
#           'q':"supermarket"}
# response = requests.get('https://places.cit.api.here.com/places/v1/discover/here', params=PARAMS)
#
# places = json.loads(response.text)['results']['items'][:]
#
# for place in places:
#     # ['position', 'distance', 'title', 'averageRating', 'category', 'icon', 'vicinity', 'having', 'type', 'href', 'id']
#     print(place['category']['id'])

#####

if __name__=='__main__':

    #Getting the API config
    with open("config.yml", 'r') as stream:
        try:
            cfg = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    HERE_ID = cfg["here_api"]["here_id"]
    HERE_PASSWD = cfg["here_api"]["here_passwd"]

    geocoderApi = herepy.GeocoderApi(HERE_ID, HERE_PASSWD)
    routingPublicTransportApi = herepy.public_transit_api.PublicTransitApi(HERE_ID, HERE_PASSWD)
    routingApi = herepy.routing_api.RoutingApi(HERE_ID, HERE_PASSWD)
    placesApi = herepy.places_api.PlacesApi(HERE_ID, HERE_PASSWD)

    #####

    start_pos_geocoder = geocoderApi.free_form('44 Tehama San Francisco CA')  #object of type GeocoderResponse
    # start_pos_geocoder = geocoderApi.free_form('298 W McKinley Sunnyvale CA')
    end_pos_geocoder = geocoderApi.free_form('111 Charles Sunnyvale CA')
    start_pos_dict = start_pos_geocoder.as_dict()['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]
    end_pos_dict = end_pos_geocoder.as_dict()['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]

    # #####
    #
    start_pos = [start_pos_dict['Latitude'], start_pos_dict['Longitude']]
    end_pos = [end_pos_dict['Latitude'], end_pos_dict['Longitude']]
    time = '2019-07-20T12:00:00'

    option_list = []
    option_list.append(getOption(start_pos, end_pos, time, "pedestrian"))
    option_list.append(getOption(start_pos, end_pos, time, "car"))
    option_list.append(getOption(start_pos, end_pos, time, "public transport"))

    displayOptions(option_list)

    closestInterest = getClosestInterest(position=[37.7874,-122.3964], type='supermarket')
    print(f'Closest interest: {closestInterest["title"]}, {closestInterest["distance"]} m away')
