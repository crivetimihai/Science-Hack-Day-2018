#!/usr/bin/env python3
""" Get the JSON data form the Raspberry Pi and insert it into the database """

# Argument parsing, requests for REST API client and variables from config.py
import requests

URL = 'http://localhost:5000/api/pi'
DB_URL = 'https://saturday-ed989.firebaseio.com/cba2bf28-4561-11e8-8d36-af8980374bd1.json'

# Retrieve remote sensor data as JSON from REST API using requests:
def get_pi(url):
    """Get JSON data from remote server running on Pi"""
    r = requests.get(url)
    return r.json()

def post_pi(DB_URL, payload):
    """Post JSON data to database"""
    r = requests.post(DB_URL, json=payload)
    return

payload = get_pi(URL)
print('Posting payload', payload)
post_pi(DB_URL, payload)
