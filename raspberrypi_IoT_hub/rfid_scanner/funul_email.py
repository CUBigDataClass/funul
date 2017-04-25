import smtplib
from firebase import firebase
from tabulate import tabulate
from email.mime.multipart import MIMEMultipart
import email.mime.text as lig
from email.mime.text import MIMEText
import email.MIMEText# import MIMEtext
'''
def sendMail(items,price):
	text = """
	Hello, Friend.

	Here is your data:

	{table}

	Regards,

	Me"""

	html = """
	<html><body><p>Hello, Friend.</p>
	<p>Here is your data:</p>
	{table}
	<p>Regards,</p>
	<p>Me</p>
	</body></html>
	"""


#def sendMail(items,price):
	text = text.format(table = tabulate(items, headers = "firstrow", tablefmt = "grid"))
	
	html =  html.format(table = tabulate(items, headers = "firstrow", tablefmt = "html"))
	
	fire = firebase.FirebaseApplication('https://funul-8cd90.firebaseio.com/', None) 
	test_var = fire.get('users', None)
	print(test_var)
	result = fire.get('/users', '/email')     

	message = MIMEMultipart ("alternative", None, [MIMEText(text), MIMEText(html,'html')] )
 	
	smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        smtpserver.login('drew.meyers@funul.io', 'drewmeyers#1')
        #text = 'You purchased ' + ', '.join(items) + ' for ' + str(price)
        smtpserver.sendmail('drew.meyers@funul.io', result, message.as_string())
        smtpserver.close()
'''
def sendMail(items,price):
	tabl_tab = tablulate
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
'''
