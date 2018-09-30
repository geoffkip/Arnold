import random
import  sqlite3
import pandas as pd

class Command(object):
    GREETING_RESPONSES = ["how can I assist you?", "how's your day going", "how can I help you?"]

    def __init__(self):
        self.commands = {
            "hi": self.return_greeting(),
            "help" : self.assist(),
            "facilities": self.return_facilities(zipcode=19143)
        }

    def handle_command(self, user, command):
        response = "<@" + user + ">: "

        if command in self.commands:
            response += self.commands[command]
        else:
            response += "Sorry I don't understand"

        return response

    def return_greeting(self):
        """If any of the words in the user's input was a greeting, return a greeting response"""
        return random.choice(Command.GREETING_RESPONSES)

    def assist(self):
        return "I can help you locate locations of facilities in your zipcode. Please enter your zipcode"

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
