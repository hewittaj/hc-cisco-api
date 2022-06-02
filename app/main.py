import json
import os
import requests
from wrapper_api import Wrapper_API

# Variables
usrPass = ""
server = ""

# Retrieve user/pass/server

infoFile = open("./app/info.json", "r")
loadedFile = json.loads(infoFile.read())

#Load info into variables
usrPass = f"{loadedFile['userId']}:{loadedFile['userPassword']}"
server = loadedFile['smaUrl']

# Setup our request using the server and username / password combo
request = Wrapper_API(server, usrPass, loadedFile['userId'], loadedFile['userPassword'])

#response = request.getAllSpamByUser("ahewitt@heartlandcoop.com")
response = request.getAllUsersSpam()

# Dump to a .json file
with open('addresses.json', 'w', encoding='utf-8') as f:
    json.dump(response, f, ensure_ascii=False, indent=4)

#print(request.status_code) # Returns status code
