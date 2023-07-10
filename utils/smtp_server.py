import smtplib
import ssl
from email.mime.text import MIMEText

port = 587
password = 'gncdljhwaypzqgio'
sender = 'loslyusar@gmai.com'
context = ssl.create_default_context()


def send_email():
    with smtplib.SMTP('smtp.gmail.com', port) as server:
        server.starttls()
        server.login(sender, password)
        receiver_email = sender
        message = MIMEText('hey')
        message['Subject'] = 'HEY!'
        server.sendmail(sender, receiver_email, message.as_string())
