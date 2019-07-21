#Author: Pierre-Louis Missler       (ref. @pndurette)
#Date: 7/20/2019
#Project: SpeaknGO


from imports import *

tts = gTTS('Hello, welcome to Speak and Go, we provide you information ')
tts.save('current_location.mp3')
os.system('start current_location.mp3')

