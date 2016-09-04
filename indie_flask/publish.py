import requests
import json
import mf2py

from pytz import timezone
from urlparse import urlparse
from dateutil.tz import tzutc
from datetime import datetime
from slugify import slugify

from indie_flask import app, celery
from indie_helper import mention_from_url

# patch JSON encoder to handle datetime objects, see http://stackoverflow.com/questions/455580/json-datetime-between-python-and-javascript#3235787
json.JSONEncoder.default = lambda self,obj: (obj.isoformat() if hasattr(obj, 'isoformat') else None)

config = app.config

def isonow():
    utcnow = datetime.now(tzutc())
    return datetime(utcnow.year, utcnow.month, utcnow.day, utcnow.hour, utcnow.minute).isoformat()

def post_id_from_url(url):
    u = urlparse(url)
    return u.path.split('/')[-1]

@celery.task
def publish(source, target):
    now = isonow() #datetime.now(timezone('UTC'))
    post_id = post_id_from_url(target)

    uparts = urlparse(source)
    
    id = slugify(u'mention-{0}-{1}'.format(uparts.hostname, uparts.path.split('?')[0].replace('/', '-')))
    endpoint = 'http://dmaczka:password@127.0.0.1:5984/myblog/{0}'.format(id)

    mentions = mention_from_url(source)
        
    data = {
        '_id': id, 
        'post_id': post_id,
        'type': 'mention',
        'link': source,
        'format': 'mf2py'
    }

    data.update(mentions)
    
    r = requests.get(endpoint)
    if r.status_code == 200:
        current = r.json()
        current.update(data)
        current['updated_at'] = now
        data = current
    else:
        data['created_at'] = now
            
    #print('PUT {0}'.format(endpoint))
    #print('data: {0}'.format(json.dumps(data)))
    r = requests.put(endpoint, json.dumps(data))
    if r.status_code not in [ 201, 202 ]:
        print('PUT {0} [{1}] ({2})'.format(endpoint, r.status_code, r.text))
