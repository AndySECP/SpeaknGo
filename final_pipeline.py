######### Imports                        #######

from imports import *
from STT_process.listener import Listener
from mobility_options_queries.routeComputer import RouteComputer

######### Greeting and request           #######

# TODO play audio file

# listen for the request
listener = Listener()
# listener.record_and_save('request')



######### Request understanding          #######

# TODO speech to text

# TODO NLP and generation of the request dictionnary


######### Request to HERE API            #######

# TODO determining type of request

dict_andy = {} #temp
flag_location = True #temp

routeComputer = RouteComputer()
if flag_location:

    # compute the GPS position corresponding to the adress
    start_pos = routeComputer.computeLatLonFromAdress('44 Tehama San Francisco CA') #temp
    end_pos = routeComputer.computeLatLonFromAdress('111 Charles Sunnyvale CA') #temp
    time = '2019-07-20T12:00:00' #temp
    transportation_types = ["car", "pedestrian", "public transport"]

    list_of_options = []
    for transportation_type in transportation_types:
        characteristics = routeComputer.getOption(start_pos, end_pos, time, transportation_type)

        print(characteristics)

# TODO generate the options

######### Presentation of the options    #######

# TODO generate the audio file



######### Choice of the preferred option #######

# listen for the request
# listener.record_and_save('final_choice')

# TODO speech to text

# TODO NLP to understand if option 1 or 2 is perferred

######### Ordering of the ride if needed #######

# TODO book ride (future work)

# TODO set reminder (future work)
