######### Imports                        #######

from imports import *
from STT_process.listener import Listener
from STT_process.google_speech_text import Voice_GGC
from mobility_options_queries.routeComputer import RouteComputer
from nlp.nlp import *

import os

######### Greeting and request           #######


listener = Listener()

greeting_text_1 = 'Hello, please say your current location'
tts = gTTS(greeting_text_1)
tts.save('greeting_text_1.mp3')
os.system('start greeting_text_1.mp3')

# listener.record_and_save('start_address_2_addresses')

greeting_text_2 = 'Hello, please say your desired destination'
tts = gTTS(greeting_text_2)
tts.save('greeting_text_2.mp3')
os.system('start greeting_text_2.mp3')

# listener.record_and_save('end_address_2_addresses')


######### Request understanding          #######

# speech to text

start_address_path = 'start_address_2_addresses.wav'
end_address_path = 'end_address_2_addresses.wav'
start_request_txt = Voice_GGC().request(start_address_path) # TODO CHANNEL ERROR
end_request_txt = Voice_GGC().request(end_address_path) # TODO CHANNEL ERROR
#drawing = Voice_GGC().draw(request_txt, "demand_1", figsize=(6,4))
print(start_request_txt)
print(end_request_txt)


# NLP and generation of the request dictionnary

start_txt = get_data(start_request_txt)
start_request = get_information(start_txt)
end_txt = get_data(end_request_txt)
end_request = get_information(end_txt)
print(start_request)
print(end_request)


######### Request to HERE API            #######

# finding alternatives

start_location = start_request['Location']
end_location = end_request['Location']
date = start_request['Date']
is_address = end_request['type'] #is_address=1 if location is a full address, is_address=0 if location is a point of interest

routeComputer = RouteComputer()

if is_address:

    # compute the GPS position corresponding to the adress
    start_pos = routeComputer.computeLatLonFromAdress(start_location)
    end_pos = routeComputer.computeLatLonFromAdress(end_location)
    transportation_types = ["car", "pedestrian", "public transport"]

    list_of_options = []
    for transportation_type in transportation_types:
        list_of_options.append(routeComputer.getOption(start_pos, end_pos, time, transportation_type))

else:
    # TODO
    pass

# proposing alternatives

print(list_of_options)

if is_address:
    pass

######### Presentation of the options    #######

#compute the statistics of the options
mean_dist = np.mean([list_opp[i]['distance'] for i in range(len(list_opp))])
mean_price = np.mean([list_opp[i]['price'] for i in range(len(list_opp))])
mean_time = np.mean([list_opp[i]['time'] for i in range(len(list_opp))])
std_dist = np.std([list_opp[i]['distance'] for i in range(len(list_opp))])
std_price = np.std([list_opp[i]['price'] for i in range(len(list_opp))])
std_time = np.std([list_opp[i]['time'] for i in range(len(list_opp))])

#add a filter: if a value is two standard deviation away or if one option proposes more than two hours of walking, we remove this option 
for i, choice in enumerate(list_opp):    
    if (choice['distance'] >= mean_dist + 2 * std_dist) or (choice['time'] >= mean_time + 2 * std_time) or (choice['price'] >= mean_time + 2 * std_time):
        del list_opp[i]
    if choice['type'] == 'pedestrian' and choice['time'] >= 120:
        del list_opp[i]

#compute the message to send to the user
proposition = 'You have {} options.'.format(len(list_opp))
for i in range(len(list_opp)):
    prop_anx = 'You can choose the {} with a distance of {} miles, that would take {} minutes, for a price of {} dollars.'.format(list_opp[i]['type'], list_opp[i]['distance'], list_opp[i]['time'], list_opp[i]['price'])
    proposition = proposition + ' ' + prop_anx
proposition = proposition + ' ' + 'Which option do you prefer?'

# TODO generate the audio file

# tts = gTTS('Here are the two options.' + {transport}[0] + 'for a duration of' +{duration}[0] + 'and a cost of'
#            {cost}[0] '.'+ 'or' + {transport}[1])'for a duration of' +{duration}[1] + 'and a cost of'
#            {cost}[1] '.'
# tts.save('options.mp3')
# os.system('start current_location.mp3')


######### Choice of the preferred option #######

# listen for the request
# listener.record_and_save('final_choice')

# TODO speech to text

s_path = 'final_choice.wav'
text = Voice_GGC().request(s_path)


# TODO NLP to understand if option 1 or 2 is perferred

######### Ordering of the ride if needed #######

# TODO book ride (future work)

# TODO set reminder (future work)
