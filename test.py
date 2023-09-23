import requests
from time import sleep

def make_request(source, target):
    return requests.post('https://hazyblue.me/webmention', { 'source': source, 'target': target })

#def query_status(url):
#    r = requests.get(url)
def check(source, target):
    r = make_request(source, target)
    print('endpoint [{0}]'.format(r.status_code))
    #assert(r.status_code in [ 201, 202 ])
    status_url = r.headers['Location']
    task_state = None
    while task_state is None or not (task_state == 'SUCCESS' or task_state == 'FAILURE'):
        sleep(0.5)
        r = requests.get(status_url)
        print('GET {0} [{1}]'.format(status_url, r.status_code))
        #assert(r.status_code == 200)
        try:
            json = r.json()
        except ValueError as e:
            print('[{0}] {1}\nValueError: {2}\nText follows:\n{3}'.format(r.status_code, r.headers, str(e), r.text))
            return r.text
        else:
            task_state = json['state']
    print(json)
    return json


if __name__ == '__main__':
    import json
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
    target = 'https://hazyblue.me/posts/2016-09-11-rethinking-bias'
    source = 'https://www.facebook.com/dmaczka/posts/10104691501984273'

    #source = 'https://hazyblue.me/posts/2014-06-02-samples-statistics-central-limit-theorem-oh-my'
    #target = ''
    res = check(source, target)
    #assert('status' in json['info'] and json['info']['status'] == 'VALID')
    #print(json.dumps(res))
