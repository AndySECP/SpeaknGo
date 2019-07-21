#Author: Pierre-Louis Missler       (ref Meryll Dindin @coricos)
#Date: 7/20/2019
#Project: Hackmobility 2019 @SF 


import wave
import os
import json
import yaml
import io
import requests

class Voice_GGC:

    def __init__(self, credentials='api-key.json'):

        crd = service_account.Credentials.from_service_account_file(credentials)
        self.stt = speech.SpeechClient(credentials=crd)
        del crd

    def request_to_vectors(self, json_request):

        txt, beg, end = [], [], []

        for result in json_request.results:
            for word in result.alternatives[0].words:
                txt.append(word.word)
                beg.append(word.start_time.seconds + word.start_time.nanos/1e9)
                end.append(word.end_time.seconds + word.end_time.nanos/1e9)

        out = dict()
        out['words'], out['starts'], out['ends'] = txt, beg, end

        return out

    def request(self, voice_path):

        fle = wave.open(voice_path, 'rb')
        rte = fle.getframerate()
        fle.close()

        arg = {'language_code': 'en-US', 'enable_word_time_offsets': True}
        cfg = types.RecognitionConfig(sample_rate_hertz=rte, **arg)

        raw = io.open(voice_path, 'rb')
        fle = types.RecognitionAudio(content=raw.read())
        raw.close()
        req = self.stt.recognize(cfg, fle)

        return self.request_to_vectors(req)


text = Voice_GGC().request(r'path_of_the wav_file')
print(text)