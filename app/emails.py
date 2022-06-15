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
from prettytable import PrettyTable

import base64
import email
import json
import smtplib, ssl

# Send email to the receiver with the html string created by generateHtml()
def sendEmails(receiverEmail, table):
    # Load smtp settings and create variables
    smtpSettings = json.loads(open('smtp_settings.json', 'r', encoding='utf-8').read())
    subject = "Summary of quarantined emails"
    body = ""
    senderEmail = smtpSettings['from_email']
    portNo = smtpSettings['port']
    smtpServer = smtpSettings['smtp_server']

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = senderEmail
    message["To"] = receiverEmail
    message["Subject"] = subject

    # Add body to email
    # message.attach(MIMEText(body, "plain"))
    message.attach(MIMEText(table, "html"))

    # The following commented out lines are if you would like to send an attachment such as a pdf
    """
    textFile = "email_summary.txt"
    # Open file in binary mode
    with open(textFile, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {textFile}",
    )
    """

    try:
        # Add attachment to message and convert message to string
        # message.attach(part)
        text = message.as_string()

        # Log in to server using secure context and send email
        server = smtplib.SMTP() # try 25, 465, 587
        # server.set_debuglevel(True) # Can flip on to view debug
        server.esmtp_features['auth'] = "LOGIN"
        server.connect(smtpServer, portNo)
        server.sendmail(senderEmail, receiverEmail, text)        
        server.close()

    except smtplib.SMTPAuthenticationError as e:
        print("Failed to authenticate, email not sent")
        print(e)
        # Close server connection
        server.close()  
    except smtplib.SMTPRecipientsRefused as e:
        print("SMTP Recipients refused, email not sent")
        print(e)
        # Close server connection
        server.close()  
    except smtplib.SMTPResponseException as e:
        print("SMTP Response Exception, email not sent")
        print(e)
        # Close server connection
        server.close()  
    else:
        print("Email sent successfully!")
        # Close server connection
        server.close()  

# Load the emails from the quarantine_emails.json file, generate the html for the email, and send the email to the user
def loadSpamEmails():
    # Variables
    fJson = json.loads(open('quarantined_mail.json', 'r', encoding='utf-8').read())
    date = ""
    fromAddress = ""
    subject = ""
    emailMessage = ""

    # Loop through json file and create table to send as email
    for email, value in fJson.items():
        # Create fields
        tableFields = ["Receiver Address", "Subject", "Date", "From Address", "Release"]
        table = PrettyTable()
        table.field_names = tableFields 

        for item in value:
            # Add info to variables
            receiver = str(item['attributes']['envelopeRecipient'][0])
            subject = item['attributes']['subject']
            date = item['attributes']['date']
            fromAddress = str(item['attributes']['fromAddress'][0])
            release = ""

            # Add row to table
            table.add_row([receiver, subject, date, fromAddress, release]) 

        # Retrieve html string from the table and generate the html string
        htmlTable =  table.get_html_string()
        fullHtml = generateHtml(htmlTable)
        
        # TODO change from my email to the variable "email"
        # Sends an email to the address in the variable "email" and a table of reported spam.
        sendEmails("ahewitt@heartlandcoop.com", fullHtml) 

# Generate the html string for the email including styling and the report table
def generateHtml(table):
    fullHtml = """
        <html>
            <head>
                <style>
                    table, th, td { border: 1px solid black; border-collapse: collapse; }
                    th, td { padding: 5px; }
                </style>
            </head>
            <p> This is a summary of the emails that were quarantined by the quarantine program. If you would like a message released please reply to this email and 
                edit the release field with a "Yes".</p>
            %s

        </html>
            """% table
    
    return fullHtml