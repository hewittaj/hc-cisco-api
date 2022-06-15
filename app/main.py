import csv
import json
from emails import *
from sorter import *
from wrapper_api import Wrapper_API

# Variables
addresses = []
all_spam = {}
emailsByUser = {}
hc_emails = 'hc_emails.csv'
response = {} 
server = ""
usrPass = ""

# Retrieve user/pass/server from json file
loadedFile = json.loads(open("./app/info.json", "r").read())

#Load API authentication info into variables
usrPass = f"{loadedFile['userId']}:{loadedFile['userPassword']}"
server = loadedFile['smaUrl']

# Setup our request using the server and username/password combo
request = Wrapper_API(server, usrPass, loadedFile['userId'], loadedFile['userPassword'])

# Open the hc_emails.csv file and read in all company emails. Retrieve all spam by user email and store in dictionary
with open(hc_emails, 'r', encoding="utf-8") as csvfile:
    datareader = list(csv.reader(csvfile))
    for row in datareader:
        response = request.getAllSpamByUser(row[1])
        if(response['data'] == None or response['data'] == ['PrimarySmtpAddress'] or response['data'] == []): 
            # If no spam for user or a header row
            # print(row[1])
            continue
        else:
            all_spam[row[1]] = response['data']
            

# Dump API response to a .json file
with open('quarantined_mail.json', 'w', encoding='utf-8') as f:
    json.dump(all_spam, f, ensure_ascii=False, indent=4)

# Load spam emails and send quarantine report to each user
loadedEmails = loadSpamEmails()

#print(request.status_code) # Returns status code for testing purposes
