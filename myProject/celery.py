"""
    Celery configuration.
"""

from __future__ import absolute_import, unicode_literals

import os
from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv()

load_dotenv(verbose=True)
env_path = os.path.join(os.path.abspath(os.path.join('.env', os.pardir)), '.env')
load_dotenv(dotenv_path=env_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myProject.settings')

app = Celery('myProject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task
def print_hello():
    print("Hello from function")


app.conf.beat_schedule = {
    'add-every-2-hour': {
        'task': 'send_notification',
        'schedule': crontab(minute='*/1')
    }
}


@app.task(bind=True)
def debug_task(self):
    """
    User task with celery option
    :param self: post wsgi request
    :param: return request
    """
    print('Request: {0!r}'.format(self.request))
