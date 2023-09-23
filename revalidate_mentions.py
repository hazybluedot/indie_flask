#!/usr/bin/env python
import requests
import json
import sys
from operator import itemgetter
import argparse as ap

if sys.version < '3':
    from urlparse import urlparse
    text_type = unicode
    text_types = [ str, unicode ]
    binary_type = str
else:
    from urllib.parse import urlparse
    text_type = str
    text_types = [ str ]
    binary_type = bytes

from indie_helper.util import follow_redirects
from indie_helper.mentions import validate, publish

dbname = 'myblog'
host = 'http://127.0.0.1'
port = 5984
ddoc = 'mention_util'

endpoint = '{host}:{port}/{dbname}/_design/{ddoc}/_view/mentions'.format(host=host,
                                                                         port=port,
                                                                         dbname=dbname,
                                                                         ddoc=ddoc)
publish_endpoint = '{host}:{port}/{dbname}/{{0}}'.format(host=host,
                                                         port=port,
                                                         dbname=dbname
                                                         )

#target_template = 'https://

if __name__ == '__main__':
    parser = ap.ArgumentParser()
    parser.add_argument('--delete','-d', type=int, default=-1, metavar='N', help='delete mentions that fail the validation check if it has remained in the failed state for at least N days')

    args = parser.parse_args()
    
    r = requests.get(endpoint)

    data = r.json()
    if 'rows' not in data.keys():
        print(json.dumps(data))
        sys.exit(1)
        
    for row in map(itemgetter('value'), r.json()['rows']):
        #print(json.dumps(row))
        source = row['source']
        target = row['target']
        post_id = row['post_id']

        # check that target resolves to post_id
        real_target, res = follow_redirects(target, 10)
        #print('{0} => {1}'.format(target, real_target))
        if urlparse(real_target).path.split('/')[-1] != post_id:
            # invalid, target does not resolve to post_id if this was
            # due to target not being reachable (e.g. network is
            # down), or due to some other error, i.e. 500, we probably
            # do not want to delete the associated mention unless the problem persists.
            pass
        
        # check that source is reachable, textual, and links back to target
        v = validate(source, target, validate_target=False)
        #if not v['verified']['state']: # and v['verified']['unchanged_since'] is greater than some length of time:, delete the webmention
        #print(v['verified'])
        if args.delete >= 0 and v['verified']['state'] is False:
            try:
                print(type(v['verified']['unchanged_since']))
            except KeyError:
                pass
                #print('no unchanged value in {0}'.format(v['verified']))
                #print(datetime.now() - v['verified']['unchanged_since'])
            #f timedelta > args.after:
        publish(source, target, publish_endpoint, **{ 'body': v.get('body', None), 'data': v })
            
