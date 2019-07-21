######### Imports                        #######

from imports import *
from STT_process.listener import Listener
from STT_process.google_speech_text import Voice_GGC
from mobility_options_queries.routeComputer import RouteComputer
from nlp.nlp import *

import os

######### Greeting and request           #######


listener = Listener()

greeting_text_1 = 'Welcome to Speak N Go, please say your current location'
tts = gTTS(greeting_text_1)
tts.save('greeting_text_1.mp3')
# os.system('afplay greeting_text_1.mp3')

# listener.record_and_save('start_address_2_addresses')

greeting_text_2 = 'And please say your desired destination'
tts = gTTS(greeting_text_2)
tts.save('greeting_text_2.mp3')
# os.system('afplay greeting_text_2.mp3')


# listener.record_and_save('end_address_2_addresses')


######### Request understanding          #######

# speech to text

start_address_path = 'start_address_supermarket.wav'
end_address_path = 'end_address_supermarket.wav'
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
is_poi = end_request['type']

routeComputer = RouteComputer()

if not is_poi:

    # compute the GPS position corresponding to the adress
    start_pos = routeComputer.computeLatLonFromAdress(start_location)
    end_pos = routeComputer.computeLatLonFromAdress(end_location)
    transportation_types = ["car", "pedestrian", "public transport"]

    list_of_options = []
    for transportation_type in transportation_types:
        list_of_options.append(routeComputer.getOptionTwoAdresses(start_pos, end_pos, time, transportation_type))

else:
    # TODO
    pass


######### Presentation of the options    #######

#compute the statistics of the options
mean_dist = np.mean([list_of_options[i]['distance'] for i in range(len(list_of_options))])
mean_price = np.mean([list_of_options[i]['price'] for i in range(len(list_of_options))])
mean_time = np.mean([list_of_options[i]['time'] for i in range(len(list_of_options))])
std_dist = np.std([list_of_options[i]['distance'] for i in range(len(list_of_options))])
std_price = np.std([list_of_options[i]['price'] for i in range(len(list_of_options))])
std_time = np.std([list_of_options[i]['time'] for i in range(len(list_of_options))])

#add a filter: if a value is two standard deviation away or if one option proposes more than two hours of walking, we remove this option
for i, choice in enumerate(list_of_options):
    if (choice['distance'] >= mean_dist + 2 * std_dist) or (choice['time'] >= mean_time + 2 * std_time) or (choice['price'] >= mean_time + 2 * std_time):
        del list_of_options[i]
    if choice['type'] == 'pedestrian' and choice['time'] >= 120:
        del list_of_options[i]

#compute the message to send to the user
proposition = 'You have {} options.'.format(len(list_of_options))
for i in range(len(list_of_options)):
    prop_anx = 'You can choose the {} with a distance of {} miles, that would take {} minutes, for a price of {} dollars.'.format(list_of_options[i]['type'], list_of_options[i]['distance'], list_of_options[i]['time'], list_of_options[i]['price'])
    proposition = proposition + ' ' + prop_anx
proposition = proposition + ' ' + 'Which option do you prefer?'

print(proposition)

# generate the audio file

tts = gTTS(proposition)
tts.save('proposition.mp3')
os.system('afplay proposition.mp3')


######### Choice of the preferred option #######

# listen for the request
listener.record_and_save('final_choice')

# speech to text

final_choice_path = 'final_choice.wav'
final_choice_text = Voice_GGC().request(final_choice_path)

print(final_choice_text)


# TODO NLP to understand if option 1 or 2 is perferred

def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 

template = ['first', 'second', 'third', 'one', 'two', 'three']
words = final_choice_text.lower().split()
out = intersection(words, template)

if len(out)>1:
    print('You sould only choose one option. Please, repeat your choice.')

if out[0] == 'one' or out[0] == 'first':
    decision = 1
if out[0] == 'two' or out[0] =='second':
    decision = 2
if out[0] == 'three' or out[0] == 'third':
    decision = 3


######### Ordering of the ride if needed #######

# TODO book ride (future work)

# TODO set reminder (future work)
