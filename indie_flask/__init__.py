from flask import Flask

from .config import Default

app = Flask(__name__)
app.config.from_object(Default)
app.config.from_envvar('APP_SETTINGS', Default)

CELERY_DISABLE_RATE_LIMITS = True
VALID_SCHEMES = [ 'http', 'https' ]

logger = get_task_logger(__name__)

from webmention import endpoint
from micropub import endpoint
