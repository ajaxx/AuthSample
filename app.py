# This is a sample 'account' management service.  It provides
# the user with access to their bank account.  You don't really
# need to do much here, but when a user presents a request to

from urllib.parse import urlencode
from flask import Flask, Blueprint, render_template, redirect
from uuid import uuid4

import service_provider

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'A not-so-secret key'
app.register_blueprint(service_provider.blueprint)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
