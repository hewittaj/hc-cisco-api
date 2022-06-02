from email.utils import getaddresses
import json


def getAddresses():
    """
    This method returns all addresses that were sent spam in the past 31 days.

    Returns:
        List: Returns a list of email addresses
    """
    # Variable declaration
    addresses = []

    # Open the json file and load it
    f = open('addresses.json', 'r', encoding='utf-8',)
    data = json.loads(f.read())

    # Loop through json file and retrieve all emails that were sent spam
    for info in data["data"]:
        addresses.append(info['attributes']['envelopeRecipient'][0])
    
    # Loop through email addresses and make lower case
    for i in range(len(addresses)):
        addresses[i] = addresses[i].lower()

    # Loop through email addresses and remove duplicates
    addresses = list(dict.fromkeys(addresses))

    addresses.sort()
    # Create a sorted and lowercase text file with all addresses
    with open("addresses.txt", "w") as outfile:
        outfile.write("\n".join(addresses))
    print(addresses)

    return addresses

getAddresses()