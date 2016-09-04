from urlparse import urlparse
import requests
from bs4 import BeautifulSoup
from exceptions import Exception

from indie_flask import app

text_types = [ 'text/html' ]
managed_hosts = app.config['MANAGED_HOSTS']

class TooManyRedirects(Exception):
    pass

class InvalidResource(Exception):
    pass

def _failure(self, source, target, reason):
    self.update_state(state='FAILURE', meta={ 'source': source, 'target': target, 'reason': reason })
    return { 'status': 'INVALID', 'reason': reason }
    #abort()
    #return { 'reason': reason }

def follow_redirects(url, max_depth):
    """perform http GET url, following any redirects up to max_depth.
    return resolved url. 
    Raises TooManyRedirects exception if max_depth is exceeded"""
    
    def _wrapped(url, depth):
        if depth > max_depth:
            raise TooManyRedirects('following redirects on {0} exceeded maximum depth of {1}'.format(url, max_depth))
        
        r = requests.head(url)
        if r.status_code in [ 301, 302 ]:
            return _wrapped(r.headers['Location'], depth+1)
        elif r.status_code in [ 200 ]:
            return url
        else:
            raise InvalidResource('{0}: received http status [{1}]'.format(url, r.status_code))
    return _wrapped(url, 0)
        
def async_validate(self, source, target):
    failure = lambda r: _failure(self, source, target, r)

    self.update_state(state='PROCESSING', meta={'source': source, 'target': target})
        
    #is target a valid resource belonging to me?
    self.update_state(state='CHECKING_TARGET')
    try:
        real_target = follow_redirects(target, 10)
    except requests.ConnectionError:
        raise InvalidResource('invalid target resource')
        
    #does target belong to me?
    url_parts = urlparse(real_target)
    if url_parts.hostname not in managed_hosts:
        print('{0} not in {1}'.format(url_parts.hostname, managed_hosts))
        raise InvalidResource('I do not manage {0}'.format(target))

    #does source exist
    self.update_state(state='RETREIVING_SOURCE')
    r = requests.get(source)
    if r.status_code != 200:
        raise InvalidResource('unable to retreive source url, got [{0}]'.format(r.status_code))

    #is source textual?
    if r.headers['content-type'].split(';')[0] not in text_types:
        return failure('source response must be textual')

    #does source actually link to target
    self.update_state(state='CHECKING_LINKBACK')
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find('a', attrs={'href': target})
    if not tag:
        return failure('source does not link to target')

    #register webmention with blog
    #TODO
    
    return { 'status': 'VALID', 'source': source, 'target': real_target }
