import herepy
import yaml

#Getting the API config
with open("config.yml", 'r') as stream:
    try:
        cfg = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

here_id = cfg["here_api"]["here_id"]
here_passwd = cfg["here_api"]["here_passwd"]

geocoderApi = herepy.GeocoderApi(here_id, here_passwd)
routingPublicTransportApi = herepy.public_transit_api.PublicTransitApi(here_id, here_passwd)
routingApi = herepy.routing_api.RoutingApi(here_id, here_passwd)

#####


start_pos_geocoder = geocoderApi.free_form('44 Tehama San Francisco CA')  #object of type GeocoderResponse
# start_pos_geocoder = geocoderApi.free_form('298 W McKinley Sunnyvale CA')
end_pos_geocoder = geocoderApi.free_form('111 Charles Sunnyvale CA')
start_pos_dict = start_pos_geocoder.as_dict()['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]
end_pos_dict = end_pos_geocoder.as_dict()['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]

#####

start_pos = [start_pos_dict['Latitude'], start_pos_dict['Longitude']]
end_pos = [end_pos_dict['Latitude'], end_pos_dict['Longitude']]
time = '2019-07-20T12:00:00'

print(start_pos)
print(end_pos)


carRouteResponse = routingApi.car_route(start_pos, end_pos)
pedestrianRouteResponse = routingApi.pedastrian_route(start_pos, end_pos)
publicTransportRouteResponse = routingApi.public_transport(start_pos, end_pos, False)

distanceCar = carRouteResponse.as_dict()['response']['route'][0]['summary']['distance'] # in meters
timeCar = carRouteResponse.as_dict()['response']['route'][0]['summary']['baseTime'] # in seconds
distancePedestrian = pedestrianRouteResponse.as_dict()['response']['route'][0]['summary']['distance'] # in meters
timePedestrian = pedestrianRouteResponse.as_dict()['response']['route'][0]['summary']['baseTime'] # in seconds
distancePublicTransport = publicTransportRouteResponse.as_dict()['response']['route'][0]['summary']['distance'] # in meters
timePublicTransport = publicTransportRouteResponse.as_dict()['response']['route'][0]['summary']['baseTime'] # in seconds

route_public_transport = routingPublicTransportApi.calculate_route(start_pos, end_pos, time)

list_of_fares = route_public_transport.as_dict()['Res']['Connections']['Connection'][0]['Tariff']['Fares'][0]['Fare']
pricePublicTransport = 0
for fare_obj in list_of_fares:
    pricePublicTransport += fare_obj['price']

priceCar = 0.80 + 0.21*timeCar/60 + 1.10*distanceCar/1000/1.6

print('Car               Distance (km): {}, Time (min): {}'.format(distanceCar/1000, timeCar/60))
print('Pedestrian        Distance (km): {}, Time (min): {}, cost ($): {}'.format(distancePedestrian/1000, timePedestrian/60, priceCar))
print('Public transport  Distance (km): {}, Time (min): {}, Cost ($): {}'.format(distancePublicTransport/1000, timePublicTransport/60, pricePublicTransport))
