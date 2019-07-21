# Author:  MISSLER Pierre-Louis
# Date:    21 July 2019
# Project: SpeaknGo

import os

from imports import *


application = Flask(__name__)

# Index
@application.route('/')

@application.route('/hello')
def hello():
    return('Hello, World!')

@application.route('/home')
def home():

    return render_template('home.html')

@application.route('/index')
def index():

    return render_template('index.html')

@application.route('/cover')
def cover():

    return render_template('cover.html')

if __name__ == '__main__':
    #application.run()
    application.run(debug=True)
