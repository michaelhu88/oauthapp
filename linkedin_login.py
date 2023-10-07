from flask import Flask, redirect, url_for, session
import uuid
import requests
from requests_oauthlib import OAuth2Session
import os

app = Flask(__name__)
app.secret_key = 'Talent_Synergy'  # Change this to a random secret key
app.config['SESSION_TYPE'] = 'filesystem'

# Replace these with your LinkedIn credentials
client_id = '862y79fkc4j2e8'
client_secret = 'Evk7TliZOCIK2umC'
authorization_base_url = 'https://www.linkedin.com/oauth/v2/authorization'
token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
redirect_uri = 'http://127.0.0.1:5000/auth/linkedin/callback'

@app.route('/')
def index():
    return 'Welcome to LinkedIn OAuth'

@app.route('/auth/linkedin')
def linkedin_auth():
    linkedin = OAuth2Session(client_id, redirect_uri=redirect_uri)
    authorization_url, state = linkedin.authorization_url(authorization_base_url)
    session['oauth_state'] = state
    return redirect(authorization_url)

@app.route('/auth/linkedin/callback')
def linkedin_callback():
    linkedin = OAuth2Session(client_id, state=session['oauth_state'], redirect_uri=redirect_uri)
    token = linkedin.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url)
    user_info = linkedin.get('https://api.linkedin.com/v2/me?projection=(id,firstName,lastName,profilePicture(displayImage~:playableStreams))')
    return f"Hello, {user_info.json()['firstName']['localized']['en_US']} {user_info.json()['lastName']['localized']['en_US']}"

if __name__ == '__main__':
    app.run(debug=True)