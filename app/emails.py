# --- Resources ---
# https://towardsdatascience.com/automate-sending-emails-with-gmail-in-python-449cc0c3c317
# https://github.com/kootenpv/yagmail

# Imports
import json
import yagmail

# Main App
user = 'ahewitt.hcoop@gmail.com'
app_password = json.loads(open('./apppassword.json').read())['app_password']

to = "ahewitt@heartlandcoop.com"

subject = "test email"
content = ['mail body content']

with yagmail.SMTP(user, app_password) as yag:
    try:
        yag.send(to, subject, content)
        print("Email sent successfully")
    except(yagmail.exceptions.YagConnectionError) as e:
        print(e)