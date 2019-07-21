#Author: Pierre-Louis Missler
#Date: 7/20/2019
#Project: SoundnGo 


from google_speech_text import Voice_GGC
from imports import *

s_path = 'sounds/start_adress_1.wav'
text = Voice_GGC().request(s_path)
drawing = Voice_GGC().draw(text, "start_adress_1", figsize=(6,4))
print(text)
print(drawing)

joblib.dump(text, 'start_adress_1.jb')


