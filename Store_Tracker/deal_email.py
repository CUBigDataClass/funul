import smtplib
from firebase import firebase


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
