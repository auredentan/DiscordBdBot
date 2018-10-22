from requests_oauthlib import OAuth2Session
import requests
import os

import json


OAUTH2_CLIENT_ID = os.getenv('WOW_API_CLIENT_ID')
OAUTH2_CLIENT_SECRET = os.getenv('WOW_API_CLIENT_SECRET')
OAUTH2_REDIRECT_URI = 'https://localhost:5000/callback'
TOKEN_URL = 'https://eu.battle.net/oauth/token'

print(OAUTH2_CLIENT_ID, OAUTH2_CLIENT_SECRET)

url = "https://eu.battle.net/oauth/token?grant_type=client_credentials&client_id={}&client_secret={}".format(OAUTH2_CLIENT_ID, OAUTH2_CLIENT_SECRET)
access_token = requests.get(url).json()['access_token']
print(access_token)
