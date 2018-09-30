import random
import  sqlite3
import pandas as pd

class Command(object):
    GREETING_RESPONSES = ["how can I assist you?", "how's your day going", "how can I help you?"]

    def __init__(self):
        pass

    def handle_message(self, user, message):
        response = "<@" + user + ">: "
        argv = message.split(" ")
        command=argv[0]

        if command == "hi":
            response += self.return_greeting()
        if command == "facilities":
            zipcode= argv[1]
            response += self.return_facilities(zipcode=zipcode)
        if command == "help":
            response += self.assist()
        return response

    def return_greeting(self):
        """If any of the words in the user's input was a greeting, return a greeting response"""
        return random.choice(Command.GREETING_RESPONSES)

    def assist(self):
        return "I can help you locate locations of facilities in your zipcode. Please enter facilities followed by your zipcode"

    def return_facilities(self,zipcode=None):
        data=[]
        database = "/Users/geoffrey.kip/Projects/slackbots/facilities.db"
        db = sqlite3.connect(database)
        cursor= db.cursor()
        sql="""SELECT * FROM (SELECT
        name_of_doctor || " " || street1 || " " ||  street2 || " " || city ||  " " || state || " " || zip || " " ||  phone as address
        FROM facilities where zip={0}) where address is not null""".format(zipcode)
        result = cursor.execute(sql)
        for row in result:
            data.append(row)
        return str(data)
