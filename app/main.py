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

request.getAllSpam("endDate=2022-6-1T00:00:00.000Z&startDate=2022-5-28T00:00:00.000Z&quarantineType=spam&orderBy=date&orderDir=asc&envelopeRecipientFilterOperator=is&envelopeRecipientFilterValue=dlee@heartlandcoop.com")

#print(request.status_code) # Returns status code