import random
import  sqlite3
import pandas as pd
from datetime import datetime
import os
import argparse

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/geoffrey.kip/Projects/Arnold/nlp_creds.json"

class Command(object):
    GREETING_RESPONSES = ["how can I assist you?", "how's your day going", "how can I help you?"]

    def __init__(self):
        pass

    def handle_message(self, user, message):
        argv = message.split(" ")
        command=argv[0]

        if command == "hi":
            response = "<@" + user + ">: " + self.return_greeting()
        elif command == "facilities":
            zipcode= argv[1]
            response = self.return_facilities(zipcode=zipcode)
        elif command == "help":
            response = "<@" + user + ">: " + self.assist()
        elif command == "sentiment":
            response = print_result(analyze(message))
        elif command == "collect":
            user=user
            data= message
            self.collect_data(user=user, data=data)
            response = "<@" + user + ">: " + "The data point and time have been recorded"
        else:
            response = "<@" + user + ">: " + "Sorry I do not understand you"
        return response

    def return_greeting(self):
        """If any of the words in the user's input was a greeting, return a greeting response"""
        return random.choice(Command.GREETING_RESPONSES)

    def assist(self):
        return "I can help you locate locations of facilities in your zipcode. Please type the word 'facilities' followed by your zipcode"

    def return_facilities(self,zipcode=None):
        data=[]
        database = "./facilities.db"
        db = sqlite3.connect(database)
        cursor= db.cursor()
        sql="""SELECT * FROM (SELECT
        name_of_doctor || " " || street1 || " " ||  street2 || " " || city ||  " " || state || " " || zip || " " ||  phone as address
        FROM facilities where zip={0}) where address is not null""".format(zipcode)
        result = cursor.execute(sql)
        for row in result:
            data.append(row)
        return data

    def collect_data(self,user=None, data=None):
        user= user
        date= datetime.now().strftime("%Y-%m-%d")
        data= data
        database = "./data_collector.db"
        db = sqlite3.connect(database)
        cursor = db.cursor()
        cursor.execute('''INSERT INTO data_collector(user, text_body, recorded_at)
                      VALUES(?,?,?)''', (user,data,date))
        db.commit()

def print_result(annotations):
    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude

    for index, sentence in enumerate(annotations.sentences):
        sentence_sentiment = sentence.sentiment.score
        print('Text has a sentiment score of {}'.format(sentence_sentiment))

    result = ('Overall Sentiment: score of {} with magnitude of {}'.format(
        score, magnitude))
    return result


def analyze(text):
    """Run a sentiment analysis request on text within a passed filename."""
    client = language.LanguageServiceClient()

    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(document=document)

    # Print the results
    return annotations
