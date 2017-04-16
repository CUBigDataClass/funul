from urllib2 import urlopen
my_ip = urlopen('http://ip.42.pl/raw').read()

print my_ip