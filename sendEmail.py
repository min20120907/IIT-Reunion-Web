# Try to log in to server and send email
import smtplib, ssl

smtp_server = "smtp.tku.edu.tw"
port = 25  # For starttls
sender_email = "reunion@localhost"

# Create a secure SSL context
message = """\
Subject: Verify Email

Please enter the following UUID for the next uploads.
UUID: """
try:
    server = smtplib.SMTP(smtp_server,port)
    server.ehlo() # Can be omitted
    server.sendmail(sender_email, "jefflin.je598@gmail.com", message+"ssfhasdfsfksgjfkasg")
    # TODO: Send email here
except Exception as e:
    # Print any error messages to stdout
    print(e)
finally:
    server.quit() 
