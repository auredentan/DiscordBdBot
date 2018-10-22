from flask import Flask, render_template, url_for, redirect, session, request, jsonify, abort
from flask_login import login_user, logout_user, login_required
from requests_oauthlib import OAuth2Session 

import os

OAUTH2_CLIENT_ID = os.environ['OAUTH2_CLIENT_ID']
OAUTH2_CLIENT_SECRET = os.environ['OAUTH2_CLIENT_SECRET']
OAUTH2_REDIRECT_URI = os.environ.get('OAUTH2_REDIRECT_UI','http://localhost:5000/confirm_login')

API_BASE_URL = os.environ.get('API_BASE_URL', 'https://discordapp.com/api')
AUTHORIZATION_BASE_URL = API_BASE_URL + '/oauth2/authorize'
TOKEN_URL = API_BASE_URL + '/oauth2/token'

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = OAUTH2_CLIENT_SECRET

if 'http://' in OAUTH2_REDIRECT_URI:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

@app.route('/')
def index():
    return render_template('index.html')

def oauth2_token_updater(token):
	session['oauth2_token'] = token

def oauth2_session(token=None, state=None, scope=None):
	return OAuth2Session(
		client_id=OAUTH2_CLIENT_ID,
		token=token,
		state=state,
		scope=scope,
		redirect_uri=OAUTH2_REDIRECT_URI,
		auto_refresh_kwargs = {
			'client_id': OAUTH2_CLIENT_ID,
			'client_secret': OAUTH2_CLIENT_SECRET,
		},
		auto_refresh_url=TOKEN_URL,
		token_updater=oauth2_token_updater)  

@app.route('/login')
def login():
    scope = ['identify', 'guilds']
    discord = oauth2_session(scope=scope)
    authorization_url, state = discord.authorization_url(AUTHORIZATION_BASE_URL)
    session['oauth2_state'] = state
    return redirect(authorization_url)

def discord_get_user(token):
    discord = oauth2_session(token=token)
    try:
        req = discord.get(API_BASE_URL + '/users/@me')
    except Exception:
        return None
    
    if req.status_code != 200:
        abort(req.status_code)
    
    user = req.json()
    session['user'] = user

    


@app.route('/confirm_login')
def callback():
    if request.values.get('error'):
        return request.values['error']
    discord = oauth2_session(state=session.get('oauth2_state'))
    token = discord.fetch_token(
        TOKEN_URL,
        client_secret=OAUTH2_CLIENT_SECRET,
        authorization_response=request.url)
    session['oauth2_token'] = token
    if not token:
        redirect(url_for('index'))

    user = discord_get_user(token)
    
    return redirect(url_for('select_server'))

@app.route('/me')
def me():
    discord = oauth2_session(token=session.get('oauth2_token'))
    user = discord.get(API_BASE_URL + '/users/@me').json()
    guilds = discord.get(API_BASE_URL + '/users/@me/guilds').json()
    connections = discord.get(API_BASE_URL + '/users/@me/connections').json()
    return jsonify(user=user, guilds=guilds, connections=connections)

def get_user_managed_servers(user, guilds):
    return list(
        filter(
            lambda g: (g['owner'] is True) or
            bool((int(g['permissions']) >> 5) & 1),
            guilds)
    )

@app.route('/servers')
def select_server():
    discord = oauth2_session(token=session.get('oauth2_token'))
    user = discord.get(API_BASE_URL + '/users/@me').json()
    guilds = discord.get(API_BASE_URL + '/users/@me/guilds').json()
    user_servers = get_user_managed_servers(user, guilds)
    return render_template('select-server.html',
                           user=user, user_servers=user_servers)


@app.route('/disabled')
def disable_cog():
    pass