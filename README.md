# Speak&Go
2019 - Project for Hackmobility 2019, merging the issues of Inclusion, Mobility and Artificial Intelligence 

## Abstract 

*"Many communities have ample transportation services for their elderly and residents with disabilities who don’t drive, but those services are often too difficult to find, according to a new national survey.*

*Eighty percent of people with a disability and 40 percent of older adults who don’t drive said they couldn’t do all the activities and errands they needed or wanted to do because they couldn’t get around, according to the survey of about 1,650 people by KRC Research for the National Aging and Disability Transportation Center.*

*Many said it had left them feeling frustrated, isolated, trapped and dependent on others."*
The Washington Post

**Speak&Go** is a project building upon this observation. Our vision is to makes transportation easy and affordable for everyone and to remove the mobility barriers that still left people isolated. To do so, we have created a service based on **Speech Recognition** and **Natural Language Processing**. The service is taking a vocal request from the user, that want to go to a place at a given time. It analyses this request and extract location and date information. Those information are used to find the desired place on the map and determine the optimal transportation option for the user (that is adapted to his personal constraints - disability or mobility difficulties). Then, it propose the best options to the user that can easily confirm the trip. In case the trip has been scheduled in advance, a reminder is set. This project especially leverages the **Here API**. 

Two UI have been created: a smartphone widget to easily request the ride and have all the information stored on the phone and a number to call to make the request for users that does not have a smartphone. 

## Speech to text

## Natural Language Processing

![NER](https://user-images.githubusercontent.com/38164557/61586711-a44f8c00-ab2f-11e9-870c-8d8bc7f91138.JPG)

Using the text generated in a json format, a NLP **Named Entity Recognition** model is used to extract relevant information out of the request. The function get_information returns a dictionary with two keys: location and date. 

## Determination of the best ride

## Service



