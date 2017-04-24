import smtplib
from firebase import firebase

def sendMail(items,price):
	fire = firebase.FirebaseApplication('https://funul-8cd90.firebaseio.com/', None)
	result = fire.get('/users', '/email')

	smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo()
	smtpserver.login('drew.meyers@funul.io', 'drewmeyers#1')
    	text = 'You purchased ' + ', '.join(items) + ' for ' + str(price)
    	smtpserver.sendmail('drew.meyers@funul.io', result, text)
    	smtpserver.close()
