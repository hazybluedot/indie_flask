class Default(object):
    DEBUG = False
    MANAGED_HOSTS = [ 'hazyblue.me', 'sofa.myblog.couchdb.local' ]
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    PUBLISH_ENDPOINT = 'http://dmaczka:password@127.0.0.1:5984/myblog/{0}'
    TIMEZONE='US/Eastern'
    TOKEN_ENDPOINT = 'https://tokens.indieauth.com/token'

class Debug(Default):
    DEBUG = True
