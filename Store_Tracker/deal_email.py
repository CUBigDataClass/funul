import smtplib
from firebase import firebase
from tabulate import tabulate
from email.mime.multipart import MIMEMultipart
import email.mime.text as lig
from email.mime.text import MIMEText
import email.MIMEText# import MIMEtext


def sendDealMail():
	#tabl_tab = tablulate
    fire = firebase.FirebaseApplication('https://funul-8cd90.firebaseio.com/', None)
    result = fire.get('/users', '/email')

    smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo()
    smtpserver.login('drew.meyers@funul.io', 'drewmeyers#1')
    text = 'Looking for some milk? We have a great deal on gallons of Organic Valley right now, 50% for the next hour!!'
    smtpserver.sendmail('drew.meyers@funul.io', result, text)
    smtpserver.close()
