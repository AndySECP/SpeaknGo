######### Imports                        #######

from imports import *
from STT_process.listener import Listener
from nlp.nlp import *

######### Greeting and request           #######

# TODO play audio file

# listen for the request
listener = Listener()
listener.record_and_save('request')



######### Request understanding          #######

# TODO speech to text

# TODO NLP and generation of the request dictionnary

txt = get_data(request_txt)
infos = get_information(txt)


######### Request to HERE API            #######

# TODO determining type of request

dict_andy = infos

# TODO generate the options

######### Presentation of the options    #######

# TODO generate the audio file



######### Choice of the preferred option #######

# listen for the request
listener.record_and_save('final_choice')

# TODO speech to text

# TODO NLP to understand if option 1 or 2 is perferred

######### Ordering of the ride if needed #######

# TODO book ride (future work)

# TODO set reminder (future work)
