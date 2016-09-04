class Default(object):
    DEBUG = False
    MANAGED_HOSTS = [ 'hazyblue.me' ]
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    PUBLISH_ENDPOINT = 'http://localhost:5984/myblog/<id>'
    TIMEZONE='US/Eastern'
    
class Debug(Default):
    DEBUG = True
