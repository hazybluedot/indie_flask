from flask import request, make_response, jsonify
import requests
from urllib2 import unquote

from indie_flask import app

def form_decode(text):
    return dict( tuple(entry.split('=')) for entry in unquote(text).split('&') )

token_endpoint = app.config['TOKEN_ENDPOINT']
pub_endpoint = app.config['PUBLISH_ENDPOINT']

class IndieAuth(requests.auth.AuthBase):
    def __init__(self, endpoint):
        self.endpoint = endpoint)
        
    def __call__(self, r):
        r = requests.get(self.endpoint, headers={ 'Authorization': auth })
        
def check_auth(token):
    r = requests.get(token_endpoint, headers={ 'Authorization': auth })
    if r.status_code == 200 and r.text:
        return form_decode(r.text)
    return None

def publish(pub):
    pub.update({
    })
    r = requests.put(endpoint, json.dumps(data))
    return r

@app.route('/webmention', methods=['POST'])
def micropub_create():
    auth = request.headers.get('Authorization')
    ident = check_auth(auth)
    if ident is None:
        return make_response('Not Authorized', 403)
    
    h = request.form['h']
    content = request.form['content']
    author=ident['me']
    if 'create' not in ident['scope'].split('+'):
        return make_respone('Scope not authorized', 403)

    res = publish(dict(
        h=h,
        content=content
        ))

    return None, 201, {'Location': status_url }
