# --- Resources ---
# https://towardsdatascience.com/automate-sending-emails-with-gmail-in-python-449cc0c3c317
# https://github.com/kootenpv/yagmail
# https://realpython.com/python-send-email/#option-2-setting-up-a-local-smtp-server

# Imports
from datetime import date
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import base64
import email
import json
import smtplib, ssl

# Main App
def sendEmails():
    # Load smtp settings and create variables
    smtpSettings = json.loads(open('smtp_settings.json', 'r', encoding='utf-8').read())
    subject = "Summary of quarantined emails"
    body = ""
    senderEmail = smtpSettings['from_email']
    receiverEmail = "ahewitt@heartlandcoop.com"
    password = smtpSettings['password']
    portNo = smtpSettings['port']
    smtpServer = smtpSettings['smtp_server']

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = senderEmail
    message["To"] = receiverEmail
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    textFile = "email_summary.txt"

    # Open file in binary mode
    with open(textFile, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {textFile}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    server = smtplib.SMTP() # try 25, 465, 587
    server.esmtp_features['auth'] = "LOGIN"
    server.connect(smtpServer, portNo)
 
    #server.set_debuglevel(True)

    server.sendmail(senderEmail, receiverEmail, text)
    server.close()


def loadSpamEmails():
    # Variables
    fJson = json.loads(open('mail_by_user.json', 'r', encoding='utf-8').read())
    date = ""
    fromAddress = ""
    subject = ""

    with open("email_summary.txt", "w", encoding='utf-8') as outfile:
        outfile.write("---Email Summary---\n")
        for email, value in fJson.items():
            
            outfile.write(f"Email: {email}\n")
            for num, item in value.items():
                #print(num)

                subject = f"SUBJECT: {item['attributes']['subject']}"
                date = f"DATE: {item['attributes']['date']}"
                fromAddress = f"FROM ADDRESS: {str(item['attributes']['fromAddress'][0])}"
                outfile.write(f"\t{date}\n")
                outfile.write(f"\t{fromAddress}\n")
                outfile.write(f"\t{subject}\n")
                outfile.write("\n")

    outfile.close()
sendEmails()
#loadSpamEmails()