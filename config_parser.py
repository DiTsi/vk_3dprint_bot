import configparser
import os


def get_string(section, key):
    parser = configparser.ConfigParser()
    parser.read(os.path.expanduser('./strings.ini'))
    a = parser.get(section, key)
    return str(a)


