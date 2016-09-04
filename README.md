# IndieWeb webmention server built on Flask

TODO: write docs

For the time being, this is an early implementation of a [webmention] receiver built on [flask].
It currently publishes webmentions to a CouchDB or similar database.

## Quick start

### Start redis

~~~~
$ bin/run_redis.sh
~~~~

Or, to use a different [Celery] [broker], start that, but remember to modify the config file.

### Start the worker

~~~~
$ celery worker -A indie_flask.celery
~~~~

### Start the flask app

~~~~
$ python run.py
~~~~

### Test

~~~~
$ source=http://somesource.com/path
$ target=http://sometarget.com/path
$ curl -X POST -d "target=$target&source=$source" http://localhost:5000/webmention
# you should get a 201 response with a status URL
# check the status:
$ curl http://localhost:5000/webmention/<status-id>
~~~~

[Celery]: http://www.celeryproject.org/
[broker]: http://docs.celeryproject.org/en/latest/getting-started/brokers/index.html
[webmention]: https://indieweb.org/webmention
[flask]: http://flask.pocoo.org/
