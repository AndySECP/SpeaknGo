# Author:  Pierre-Louis Missler
# Date:    21 July 2019
# Project: Speakngo

import os
import json
import yaml
import warnings
import requests

from flask import Flask, request, render_template, flash, redirect, url_for, session, logging
from passlib.hash import sha256_crypt
from functools import wraps
