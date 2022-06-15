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

# Main App
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

    # textFile = "email_summary.txt"

    # # Open file in binary mode
    # with open(textFile, "rb") as attachment:
    #     # Add file as application/octet-stream
    #     # Email client can usually download this automatically as attachment
    #     part = MIMEBase("application", "octet-stream")
    #     part.set_payload(attachment.read())

    # # Encode file in ASCII characters to send by email
    # encoders.encode_base64(part)

    # # Add header
    # part.add_header(
    #     "Content-Disposition",
    #     f"attachment; filename= {textFile}",
    # )

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
        htmlTable =  table.get_html_string()
        fullHtml = generateHtml(htmlTable)
        
        #TODO change from my email to the variable "email"
        sendEmails("ahewitt@heartlandcoop.com", fullHtml) # sends an email to the address and a table of the info
        # emailMessage = ""


    # Version where you can write it to a file and then send the file
    # with open("email_summary.txt", "w", encoding='utf-8') as outfile:
    #     outfile.write("---Email Summary---\n")
    #     for email, value in fJson.items():
            
    #         outfile.write(f"Email: {email}\n")
    #         for item in value:
    #             #print(num)

    #             subject = f"SUBJECT: {item['attributes']['subject']}"
    #             date = f"DATE: {item['attributes']['date']}"
    #             fromAddress = f"FROM ADDRESS: {str(item['attributes']['fromAddress'][0])}"
    #             outfile.write(f"\t{date}\n")
    #             outfile.write(f"\t{fromAddress}\n")
    #             outfile.write(f"\t{subject}\n")
    #             outfile.write("\n")

    # outfile.close()

# Generate the html string for the email including styling and table
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