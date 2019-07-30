######### Imports                        #######

from imports import *
from STT_process.listener import Listener
from STT_process.google_speech_text import Voice_GGC
from mobility_options_queries.routeComputer import RouteComputer
from nlp.nlp import *

_ = input('\nPress enter to start call')

######### Greeting and request           #######


listener = Listener(7)

greeting_text_1 = 'Welcome to Speak N Go, please say your current location'
tts = gTTS(greeting_text_1)
tts.save('greeting_text_1.mp3')
os.system('afplay greeting_text_1.mp3')

# listener.record_and_save('start_address_2_addresses')

greeting_text_2 = 'And please say your desired destination'
tts = gTTS(greeting_text_2)
tts.save('greeting_text_2.mp3')
os.system('afplay greeting_text_2.mp3')


# listener.record_and_save('end_address_2_addresses')


######### Request understanding          #######

# speech to text

start_address_path = 'start_address_2_addresses.wav'
end_address_path = 'end_address_2_addresses.wav'
start_request_txt = Voice_GGC().request(start_address_path) # TODO CHANNEL ERROR
end_request_txt = Voice_GGC().request(end_address_path) # TODO CHANNEL ERROR
# drawing = Voice_GGC().draw(start_address_path, "demand_1", figsize=(6,4))
# drawing = Voice_GGC().draw(end_address_path, "demand_1", figsize=(6,4))
print('\n')
print('Start location: ', ' '.join(word for word in start_request_txt['words']))
print('Destination:    ', ' '.join(word for word in end_request_txt['words']))
print('\n')


# NLP and generation of the request dictionnary

start_txt = get_data(start_request_txt)
start_request = get_information(start_txt)
end_txt = get_data(end_request_txt)
end_request = get_information(end_txt)


######### Request to HERE API            #######

# finding alternatives
start_location = start_request['Location']
end_location = end_request['Location']
date = start_request['Date']
is_poi = end_request['type']

routeComputer = RouteComputer()

# if a destination address is given, use it
if not is_poi:
    # compute the GPS position corresponding to the adress
    start_pos = routeComputer.computeLatLonFromAdress(start_location)
    end_pos = routeComputer.computeLatLonFromAdress(end_location)
    transportation_types = ["car", "pedestrian", "public transport"]

    list_of_options = []
    for transportation_type in transportation_types:
        new_option = routeComputer.getOptionTwoAdresses(start_pos, end_pos, time, transportation_type)
        if new_option != None:
            list_of_options.append(new_option)

# if a POI is given, find the best option
else:
    start_pos = routeComputer.computeLatLonFromAdress(start_location)
    poi_name = end_request['Location']
    poi = routeComputer.getClosestInterest(start_pos, poi_name)
    poi_title = poi['title']
    end_pos = poi['position']

    tts = gTTS('The closest ' + poi_name + ' is ' + poi_title)
    tts.save('poi_info.mp3')
    os.system('afplay poi_info.mp3')

    transportation_types = ["car", "by foot", "public transport"]

    list_of_options = []
    for transportation_type in transportation_types:
        new_option = routeComputer.getOptionTwoAdresses(start_pos, end_pos, time, transportation_type)
        if new_option != None:
            list_of_options.append(new_option)

for i, option in enumerate(list_of_options):
    print('OPTION n°{}'.format(i+1))
    print('Type:     ', option['type'])
    print('Distance: ', option['distance'])
    print('Price:    ', option['price'])
    print('Time:     ', option['time'])
    print('\n')

######### Presentation of the options    #######

#compute the statistics of the options
compute_stats = False
if compute_stats:
    mean_dist = np.mean([list_of_options[i]['distance'] for i in range(len(list_of_options))])
    mean_price = np.mean([list_of_options[i]['price'] for i in range(len(list_of_options))])
    mean_time = np.mean([list_of_options[i]['time'] for i in range(len(list_of_options))])
    std_dist = np.std([list_of_options[i]['distance'] for i in range(len(list_of_options))])
    std_price = np.std([list_of_options[i]['price'] for i in range(len(list_of_options))])
    std_time = np.std([list_of_options[i]['time'] for i in range(len(list_of_options))])

#add a filter: if a value is two standard deviation away or if one option proposes more than two hours of walking, we remove this option
for i, choice in enumerate(list_of_options):
    # if (choice['distance'] >= mean_dist + 2 * std_dist) or (choice['time'] >= mean_time + 2 * std_time) or (choice['price'] >= mean_time + 2 * std_time):
    #     del list_of_options[i]
    if choice['type'] == 'by foot' and choice['time'] >= 120:
        del list_of_options[i]

#compute the message to send to the user
proposition = 'You have {} options.'.format(len(list_of_options))
for i in range(len(list_of_options)):
    prop_anx = 'You can choose the {}, taking {} minutes, and costing {} dollars.'.format(list_of_options[i]['type'], int(list_of_options[i]['distance']), int(list_of_options[i]['time']), int(list_of_options[i]['price']))
    proposition = proposition + ' ' + prop_anx
proposition = proposition + ' ' + 'Which option do you prefer?'

# generate the audio file

tts = gTTS(proposition)
tts.save('proposition.mp3')
os.system('afplay proposition.mp3')


######### Choice of the preferred option #######

decision = None
while decision == None:
    # listen for the request
    listener = Listener(4)
    listener.record_and_save('final_choice')

    # speech to text
    final_choice_path = 'final_choice.wav'
    final_choice_text = Voice_GGC().request(final_choice_path)

    print('Response: ', ' '.join(word for word in final_choice_text['words']))

    # NLP to understand if option 1 or 2 is perferred

    def intersection(lst1, lst2):
        lst3 = [value for value in lst1 if value in lst2]
        return lst3

    template = ['first', 'second', 'third', 'one', 'two', 'three', 'to', '1', '2', '3']
    words = ' '.join(word for word in final_choice_text['words']).lower().split()
    out = list(set(intersection(words, template)))

    if len(out)>1:
        tts = gTTS('Please choose only one option')
        tts.save('error_message.mp3')
        os.system('afplay error_message.mp3')
        continue

    elif len(out) == 0:
        tts = gTTS('Please choose an option')
        tts.save('error_message.mp3')
        os.system('afplay error_message.mp3')
        continue

    else:
        if out[0] == 'one' or out[0] == 'first' or out[0] == '1':
            decision = 0
        if out[0] == 'two' or out[0] =='second' or out[0] =='to' or out[0] == '2':
            decision = 1
        if out[0] == 'three' or out[0] == 'third' or out[0] == '3':
            decision = 2

print('Option chosen: ', list_of_options[decision]['type'])

######### Recap #######

if list_of_options[decision]['type'] == 'car':
    transportation_mode = 'take the car. '
    additional_message = 'A mobility service ride has been requested. '
elif list_of_options[decision]['type'] == 'by foot':
    transportation_mode = 'go by foot. '
    additional_message = ''
elif list_of_options[decision]['type'] == 'public transport':
    transportation_mode = 'take the public transportations. '
    additional_message = ''


recap = 'You have chosen to ' + transportation_mode + additional_message + 'Goodbye.'
tts = gTTS(recap)
tts.save('recap.mp3')
os.system('afplay recap.mp3')
