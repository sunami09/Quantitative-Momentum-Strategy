from apikey import *
from urllib.request import urlopen
import certifi
import ssl
import json
import sys


cert = ssl.create_default_context()
cert.load_verify_locations(cafile=certifi.where())



def get_data(url):
    response = urlopen(url, context=cert)
    if response.getcode() == 200:
        print("API Call Successful")
    else:
        print("APi call failed")
        sys.exit()
    return json.load(response)