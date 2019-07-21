#Author: Pierre-Louis Missler       (ref. Meryll Dindin @coricos)
#Date: 7/20/2019
#Project: Hackmobility 2019 @SF


import wave
import io
import numpy as np
import pandas as pd

# Needed for visualisation
import matplotlib.pyplot as plt

# Google Cloud package
from google.oauth2 import service_account
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

class Voice_GGC:

    def __init__(self, credentials='STT_process/api-key.json'):

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

    def draw(self, request, title=None, figsize=(18,6)):

        df = pd.DataFrame.from_dict(request)
        fig, ax = plt.subplots(figsize=figsize)

        begin, stops, names = df.starts.values, df.ends.values, df.words.values
        # Create the base line
        start, stop = min(begin), max(stops)
        ax.plot((start, stop), (0, 0), 'k', alpha=.5)

        for ii, (iname, istart, istop) in enumerate(zip(names, begin, stops)):

            level = np.asarray([0.3, 0.6])[ii % 2]
            vert = 'top' if level < 0 else 'bottom'
            ax.scatter(istart, 0, s=100, facecolor='salmon', edgecolor='crimson', zorder=9999)
            ax.plot((istart, istart), (0, 1), c='dodgerblue', alpha=.5)
            ax.bar(istart, level, width=istop-istart, align='edge', color='tomato', alpha=0.0)
            arg = {'horizontalalignment': 'center', 'verticalalignment': vert}
            ax.text(istart + (istop-istart)/2, level, iname, fontsize=14, backgroundcolor=(0, 0, 0, 0), rotation=90, **arg)

        fig.suptitle(title, fontsize=16)
        fig.autofmt_xdate()
        plt.setp((ax.get_yticklabels() + ax.get_yticklines() + list(ax.spines.values())), visible=False)
        plt.show()
        ax.bar(istop, level, width=1000, align='edge', color='lightblue', alpha=0.5)
#
#text = Voice_GGC().request(r'C:\Users\pierr\Google Drive\UC BERKELEY MEng\HackMobility\service_STT\test_hackathon.wav')
#drawing = Voice_GGC().draw(text, None, figsize=(18,6))
#print(text)
#print(drawing)
