from datetime import datetime, timedelta
from time import strftime
from urllib.request import HTTPBasicAuthHandler
from requests.auth import HTTPBasicAuth
import requests
import sys
import requests
import base64
import json


# Next lines turn off messages about missing SSL certificates
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Wrapper_API(object):
    """
    Initialisation for the class dealing with all calls to the FMC API
    """

    def __init__(self, server, usrPass, userName, password):
        b64Val = base64.b64encode(bytes(usrPass, "UTF-8"))
        self.userName = userName
        self.password = password
        self.server = server
        self.usrPass = b64Val
        self.headers = {'Content-Type': 'application/json',
                        "Authorization": "Basic %s" % self.usrPass,
                        "Cookie": "sid=BnmbzphnMPdDBmVTpMku",
                        "Connection": "keep-alive"}
        self.api_base_path = "/sma/api/v2.0/quarantine/messages?"
        self.json_resp = {}

    def getAllUsersSpam(self):
        """
        Generic GET request to the ESA API with exception handling to retrieve all spam that was quarantined for all users.

        Parameters
        -------
        self : Wrapper_API
            Object representing the API String to use.

        Returns
        -------
        Returns a json dump of all spam for all users.
        """

        url = ""
        # Get end date dynamically from today to last month/31 days
        endDate = datetime.now().isoformat(timespec="minutes")
        startDate = (datetime.fromisoformat(endDate) - timedelta(days=31)).isoformat(timespec="minutes")
        
        # Build url NOTE: timestamp seconds and milliseconds must be in all zeroes
        url = f"endDate={endDate}:00.000Z&startDate={startDate}:00.000Z&" + "quarantineType=spam&orderBy=date&orderDir=asc"

        ApiPath = self.server + self.api_base_path + url
        try:
            r = requests.get(ApiPath, headers=self.headers, verify=False, auth=HTTPBasicAuth(self.userName, self.password))
            status_code = r.status_code
            resp = r.text
            if (status_code == 200):
                self.json_resp = json.loads(resp)
                #print(self.json_resp) # Remove comment if testing
                return self.json_resp
            else:
                r.raise_for_status()
                print("Error occurred in GET --> "+resp)
        except requests.exceptions.HTTPError as err:
            print("Error in connection --> "+str(err))
        finally:
            if r:
                r.close()

    def getAllSpamByUser(self, userEmail):
        """
        Generic GET request to the ESA API with exception handling to retrieve 
        all spam that was quarantined for a specific user.

        Parameters
        -------
        self : Wrapper_API
            Object representing the API String to use.

        userEmail : string
            Email of the user to return all spam for

        Returns
        -------
        Returns a json dump of all spam for specific user
        """

        url = ""
        # Get end date dynamically from past 7 days
        endDate = datetime.now().isoformat(timespec="minutes")
        startDate = (datetime.fromisoformat(endDate) - timedelta(days=7)).isoformat(timespec="minutes")
        
        # Build url NOTE: timestamp seconds and milliseconds must be in all zeroes
        url = f"endDate={endDate}:00.000Z&startDate={startDate}:00.000Z&" + "quarantineType=spam&orderBy=date" + "&orderDir=asc&envelopeRecipientFilterOperator=is&envelopeRecipientFilterValue=" + f"{userEmail}"

        ApiPath = self.server + self.api_base_path + url
        try:
            r = requests.get(ApiPath, headers=self.headers, verify=False, auth=HTTPBasicAuth(self.userName, self.password))
            status_code = r.status_code
            resp = r.text
            if (status_code == 200):
                self.json_resp = json.loads(resp)
                #print(self.json_resp) # Remove comment if testing
                return self.json_resp
            else:
                r.raise_for_status()
                print("Error occurred in GET --> "+resp)
        except requests.exceptions.HTTPError as err:
            print("Error in connection --> "+str(err))
        finally:
            if r:
                r.close()
