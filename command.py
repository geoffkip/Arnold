import random
import  sqlite3
import pandas as pd
from datetime import datetime

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
