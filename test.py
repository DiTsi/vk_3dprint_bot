import configparser
import os

parser = configparser.ConfigParser()

parser.read(os.path.expanduser('./strings.ini'))
a = parser.get('strings', 'messages')
print(a)
exit(0)


