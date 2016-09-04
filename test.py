import requests
from time import sleep

def make_request(source, target):
    return requests.post('http://localhost:5000/webmention', { 'source': source, 'target': target })

#def query_status(url):
#    r = requests.get(url)
def check(source, target):
    r = make_request(source, target)
    assert(r.status_code in [ 201, 202 ])
    status_url = r.headers['Location']
    task_state = None
    while task_state is None or not (task_state == 'SUCCESS' or task_state == 'FAILURE'):
        sleep(0.5)
        r = requests.get(status_url)
        #assert(r.status_code == 200)
        try:
            json = r.json()
        except ValueError:
            print('[{0}] {1} {2}'.format(r.status_code, r.headers, r.text))
            return r.text()
        else:
            task_state = json['state']
    print(json)
    return json


if __name__ == '__main__':
    # # INVAILD, target is not managed by me
    # target = 'https://github.com/hazybluedot'
    # source = 'https://hazyblue.me'
    # json = check(source, target)
    # assert(json['info']['status'] == 'INVALID')
    
    # # INVALID, source does not link to target
    # target = 'https://hazyblue.me'
    # source = 'https://github.com'
    # json = check(source, target)
    # assert(json['info']['status'] == 'INVALID')

    # # INVALID, target is not 200
    # target = 'https://hazyblue.me/invalid'
    # source = 'https://github.com/hazybluedot'
    # json = check(source, target)
    # assert(json['info']['status'] == 'INVALID')

    # VALID
    # target = 'https://hazyblue.me/posts/2015-10-31-word-vs-latex-and-other-meaningless-comparisons'
    target = 'https://t.co/gQitTIDSgV'
    source = 'https://twitter.com/gRegorLove/status/770387402430877696'

    #source = 'https://hazyblue.me/posts/2014-06-02-samples-statistics-central-limit-theorem-oh-my'
    #target = ''
    json = check(source, target)
    assert('status' in json['info'] and json['info']['status'] == 'VALID')
