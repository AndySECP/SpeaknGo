#NLP Information Extraction
#Get the information for the request to the API

#imports
import spacy
from spacy import displacy
from collections import Counter
import joblib
import argparse
import json
import numpy as np

nlp = spacy.load("en_core_web_sm")


def get_data(file):
	''' This function get the data from the json file '''

	#Extract request text information from the json / joblib file
	# try:
	# 	doc = joblib.load(file)
	# except:
	# 	doc = json.load(open(file, 'r'))
	# else:
	# 	doc = file

	doc = file

	#Transform the list of tokens into a single string
	final = ' '.join(nlp(token).text_with_ws for token in doc["words"])

	return final


#Extract location and date information using Scipy library

def get_information(txt):
	'''This function return the place to go and the time we should go.'''

	doc = nlp(str(txt))

	infos = {'Location':'', 'Date':''}
	loc_starts, loc_ends = [], []

	#check what part of the string correspond to the location and to the date
	try:
		for ent in doc.ents:
			if ent.label_ in ['CARDINAL', 'LOC', 'ORG', 'FAC', 'GPE']:
				loc_starts.append(ent.start_char)
				loc_ends.append(ent.end_char)
			if ent.label_ in ['TIME', 'DATE']:
				infos['Date'] = infos['Date'] + ' ' + ent.text
		txt_ = str(doc)
		infos['Location'] = txt_[min(loc_starts):max(loc_ends)+1]
	except:
		pass

    #check if the location is an address or a point of interest
	is_poi = True
	loc = infos['Location']
	if any(char.isdigit() for char in loc): is_poi = False
	if 'street' in loc.lower(): is_poi = False
	if 'avenue' in loc.lower(): is_poi = False
	infos['type'] = int(is_poi)

	if is_poi:
		list_txt = txt.split(' ')
		longest_length = len(list_txt[0])
		longest_word = list_txt[0]
		for word in list_txt[1:]:
			if len(word) > longest_length:
				longest_length = len(word)
				longest_word = word

		infos['Location'] = longest_word

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
