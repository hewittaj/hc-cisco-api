# --- Resources ---
# https://towardsdatascience.com/automate-sending-emails-with-gmail-in-python-449cc0c3c317
# https://github.com/kootenpv/yagmail

# Imports
from datetime import date
import json
import yagmail

# Main App
def sendEmails():
    # Variables
    user = 'ahewitt.hcoop@gmail.com'
    app_password = json.loads(open('./apppassword.json').read())['app_password']
    to = "ahewitt@heartlandcoop.com"
    subject = "test email"
    content = ['mail body content']

    # Send email
    with yagmail.SMTP(user, app_password) as yag:
        try:
            yag.send(to, subject, content)
            print("Email sent successfully")
        except(yagmail.exceptions.YagConnectionError) as e:
            print(e)

def loadSpamEmails():
    # Variables
    fJson = json.loads(open('mail_by_user.json', 'r', encoding='utf-8').read())
    date = ""
    fromAddress = ""
    subject = ""
    
    for email, value in fJson.items():
        print(email)
        for num, item in value.items():
            #print(num)

            f"{item['attributes']['subject']}"
            f"{item['attributes']['date']}"
            f"{str(item['attributes']['fromAddress'][0])}"

loadSpamEmails()