import smtplib

smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo()
smtpserver.login('drew.meyers@funul.io', 'drewmeyers#1')
smtpserver.sendmail('drew.meyers@funul.io', 'brandon.spitler@colorado.edu', 'wassup dude')
smtpserver.close()
