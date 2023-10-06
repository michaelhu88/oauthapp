from flask import Flask, redirect, url_for, session
from flask_oauthlib.client import OAuth
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'random_secret_key'
app.debug = True
oauth = OAuth(app)

linkedin = oauth.remote_app(
    'linkedin',
    consumer_key='YOUR_LINKEDIN_CLIENT_ID',
    consumer_secret='YOUR_LINKEDIN_CLIENT_SECRET',
    request_token_params={
        'scope': 'r_liteprofile r_emailaddress',
        'state': 'RandomString',
    },
    base_url='https://api.linkedin.com/v2/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://www.linkedin.com/oauth/v2/accessToken',
    authorize_url='https://www.linkedin.com/oauth/v2/authorization',
)

@app.route('/')
def index():
    return 'Welcome! Please <a href="/login">login</a>.'

@app.route('/login')
def login():
    return linkedin.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.pop('linkedin_token')
    return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
    response = linkedin.authorized_response()
    
    if response is None or response.get('error'):
        return 'Access denied: reason={} error={}'.format(
            response.get('error_reason'),
            response.get('error_description')
        )

    session['linkedin_token'] = (response['access_token'], '')
    me = linkedin.get('me')
    
    return 'Logged in as: ' + me.data['firstName']

@linkedin.tokengetter
def get_linkedin_oauth_token():
    return session.get('linkedin_token')

if __name__ == '__main__':
    app.run()