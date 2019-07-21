######### Imports                        #######

from imports import *
from listener import Listener

######### Greeting and request           #######

# TODO play audio file

# listen for the request
listener = Listener('request')
listener.record_and_save()



######### Request understanding          #######

# TODO speech to text

# TODO NLP and generation of the request dictionnary


######### Request to HERE API            #######

# TODO determining type of request

# TODO generate the options

######### Presentation of the options    #######

# TODO generate the audio file



######### Choice of the preferred option #######

# TODO listen for the request

# TODO speech to text

# TODO NLP to understand if option 1 or 2 is perferred

######### Ordering of the ride if needed #######

# TODO book ride (future work)

# TODO set remider (future work)
