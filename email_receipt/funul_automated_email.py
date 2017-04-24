import smtplib
from firebase import firebase

fire = firebase.FirebaseApplication('https://funul-8cd90.firebaseio.com/', None)
result = fire.get('/users', '/email')

smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo()
smtpserver.login('drew.meyers@funul.io', 'drewmeyers#1')
smtpserver.sendmail('drew.meyers@funul.io', result, 'wassup dude')
smtpserver.close()
