import json
from emails import *
from sorter import *
from wrapper_api import Wrapper_API

# Variables
usrPass = ""
server = ""
addresses = []
emailsByUser = {}

# Retrieve user/pass/server

infoFile = open("./app/info.json", "r")
loadedFile = json.loads(infoFile.read())

#Load info into variables
usrPass = f"{loadedFile['userId']}:{loadedFile['userPassword']}"
server = loadedFile['smaUrl']

# Setup our request using the server and username / password combo
request = Wrapper_API(server, usrPass, loadedFile['userId'], loadedFile['userPassword'])

response = request.getAllUsersSpam()

# Dump API response to a .json file
with open('quarantined_mail.json', 'w', encoding='utf-8') as f:
    json.dump(response, f, ensure_ascii=False, indent=4)

# Get addresses and load into a list
addresses = getAddresses()

# Get emails by each user and load it into dictionary
emailsByUser = getEmailsByUser(addresses)

# Load spam emails and send to each user
loadedEmails = loadSpamEmails()
sendEmails()

#print(request.status_code) # Returns status code
