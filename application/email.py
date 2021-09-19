import smtplib
from config import Config


def send_email(recipient, message):
    sender_mail = Config.MAIL_USERNAME
    password = Config.MAIL_PASSWORD
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(sender_mail, password)
    server.sendmail(sender_mail, recipient, message)
