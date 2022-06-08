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

# Retrieve user/pass/server

loadedFile = json.loads(open("./app/info.json", "r").read())

#Load info into variables
usrPass = f"{loadedFile['userId']}:{loadedFile['userPassword']}"
server = loadedFile['smaUrl']

# Setup our request using the server and username / password combo
request = Wrapper_API(server, usrPass, loadedFile['userId'], loadedFile['userPassword'])

# Alternate way
# response = request.getAllUsersSpam() # Gets all spam for all users, not specifying an email address

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

# Get addresses and load into a list
# addresses = getAddresses()

# Get emails by each user and load it into dictionary
# emailsByUser = getEmailsByUser(addresses)

# Load spam emails and send to each user
loadedEmails = loadSpamEmails()
# sendEmails()

#print(request.status_code) # Returns status code
