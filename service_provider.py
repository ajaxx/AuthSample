from urllib.parse import urlencode
from flask import Flask, Blueprint, make_response, render_template, redirect, request, url_for, session
from uuid import uuid4

import http.client
import json
import requests
import os, os.path

# obviously you would not use this, but its the prefix that is
# exposed for this test
client_url_prefix = 'http://localhost:5000'
# the client endpoint (for redirect)
client_endpoint_url = f"{client_url_prefix}/authorization-code/callback"

with open(os.path.join(os.path.dirname(__file__), 'service_provider.json')) as fh:
    client_service_configuration = json.load(fh)
    client_id = client_service_configuration['client_id']
    client_secret = client_service_configuration['client_secret']
    authorization_endpoint = client_service_configuration['authorization_endpoint']
    token_endpoint = client_service_configuration['token_endpoint']
    scope = client_service_configuration['scope']

# Blueprint for static pages
blueprint = Blueprint('service_provider', __name__, static_folder='static', template_folder='templates')

@blueprint.route('/authorization-code/callback')
def authorization_code():
    # Section (C):
    # Assuming the resource owner grants access, the authorization
    # server redirects the user-agent back to the client using the
    # redirection URI provided earlier (in the request or during
    # client registration).  The redirection URI includes an
    # authorization code and any local state provided by the client
    # earlier.
    request_args = request.args

    # first, lets validate that everything is here
    assert('code' in request_args) # required - see 4.1.2
    assert('state' in request_args) # required - see 4.1.2

    # validate the state against the session state
    oauth2_state = request.cookies.get('oauth2_state')
    assert(oauth2_state is not None)
    assert(oauth2_state == request_args['state'])

    oauth2_code = request_args['code']

    # Section (D):
    # The client requests an access token from the authorization
    # server's token endpoint by including the authorization code
    # received in the previous step.  When making the request, the
    # client authenticates with the authorization server.  The client
    # includes the redirection URI used to obtain the authorization
    # code for verification.

    client_endpoint_path = url_for('service_provider.authorization_code')

    token_exchange_params = {
        'grant_type' : 'authorization_code',  # required - see 4.1.3
        'client_id' : client_id,              # required - see 4.1.3
        'client_secret' : client_secret,      # depends on server authorization
        'redirect_uri' : client_endpoint_url, # required - see 4.1.3
        'code' : oauth2_code                  # required - see 4.1.3
    }

    token_response = requests.post(token_endpoint, token_exchange_params)
    assert(token_response.status_code == 200)

    print(f'Exchanging code {oauth2_code} for access token')

    token_response = json.loads(token_response.text)

    return render_template('authorization_response.html', data = token_response)

@blueprint.route('/authorize')
def authorize():
    # Section (A):
    # The client initiates the flow by directing the resource owner's
    # user-agent to the authorization endpoint.  The client includes 
    # its client identifier, requested scope, local state, and a
    # redirection URI to which the authorization server will send the 
    # user-agent back once access is granted (or denied).

    # generate our own random state
    state = str(uuid4())
    # our application parameters
    oauth_params = {
        'response_type' : 'code',
        'client_id' : client_id,
        'redirect_uri' : client_endpoint_url,
        'scope' : scope,
        'state' : state
    }

    redirect_url = authorization_endpoint + '?' + urlencode(oauth_params)
    response = make_response(redirect(redirect_url))
    response.set_cookie('oauth2_state', state)
    return response
