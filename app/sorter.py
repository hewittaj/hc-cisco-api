import json
from operator import itemgetter

def getAddresses():
    """
    This method returns all addresses that were sent spam in the past 31 days.

    Returns:
        List: Returns a list of email addresses
    """
    # Variable declaration
    addresses = []

    # Open the json file and load it
    f = open('quarantined_mail.json', 'r', encoding='utf-8',)
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
    # Create a sorted and lowercase text file with all addresses.
    # Will be used to send emails to each person a summary of 
    # quarantined email(s).
    with open("addresses.txt", "w") as outfile:
        outfile.write("\n".join(addresses))
    
    # Close file
    f.close()

    return addresses

def getEmailsByUser(addresses):
    # Variable declaration
    mailByUser = {}
    tmp = {}
    i = 0

    # Load quarantined_mail json 
    fJson = open('quarantined_mail.json', 'r', encoding='utf-8')
    dataJson = json.loads(fJson.read())

    # Moving down levels to be able to sort
    dataJson = dataJson["data"]

    # Loop through emails in addresses and compare against quarantined
    # emails. Add matches to dictionary
    for email in addresses:
        for item in dataJson:
            lowercase = str(item['attributes']['envelopeRecipient'][0]).lower()
            if email == lowercase:
                tmp.update({str(i): item})
                i += 1
        mailByUser.update({email:tmp})
        tmp = {}
        i = 0

    # Dump python dictionary to json
    with open('mail_by_user.json', 'w', encoding='utf-8') as f:
        json.dump(mailByUser, f, ensure_ascii=False, indent=4)

    # Close files
    fJson.close()

    return mailByUser
