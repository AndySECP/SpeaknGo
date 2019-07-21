# Author: Pierre-Louis Missler
# Date:    7/20/2019
# Project: SoundnGO

import io
import os
import time
import yaml
import json
import wave
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib
import pyaudio
import spacy
import argparse
import en_core_web_sm
import pyaudio
import herepy
import requests

# Google Cloud package
from google.oauth2 import service_account
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
