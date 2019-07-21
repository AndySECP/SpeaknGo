#NLP Information Extraction
#Get the information for the request to the API

#imports
import spacy
from spacy import displacy
from collections import Counter
from pprint import pprint
import json
import argparse
nlp = spacy.load("en_core_web_sm")


def get_data(file):
	''' This function get the data from the json file '''

	#Extract request text information from the json file
	doc = json.load(open(file, 'r'))
	#Transform the list of tokens into a single string
	final = ' '.join(nlp(token).text_with_ws for token in doc["words"])

	return final


#Extract location and date information using Scipy library

def get_information(txt):
    
    '''This function return the place to go and the time we should go.'''

    doc = nlp(str(txt))
    anx = [(X.text, X.label_) for X in doc.ents]
    
    infos = {'Location':'', 'Date':''}
    
    for tuple_ in anx:
        if tuple_[1] in ['CARDINAL', 'LOC', 'ORG', 'FAC']:
            infos['Location'] = infos['Location'] + ' ' + tuple_[0]
        if tuple_[1] in ['TIME', 'DATE']:
            infos['Date'] = infos['Date'] + ' ' + tuple_[0]
            
    return infos


if __name__ == '__main__':

    # Initialize the arguments
    prs = argparse.ArgumentParser()    
    prs.add_argument('-r', '--request', help='Request file', type=str, default='request.json')
    prs = prs.parse_args()

    print('# Getting the location and date information')
    txt = get_data(prs.request)
    infos = get_information(txt)
    print(infos)