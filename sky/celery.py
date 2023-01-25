import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sky.settings')
app = Celery('sky')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'verify-files': {
        'task': 'app.tasks.verify_file',
        'schedule': crontab(minute='*/3'),
    },

    'check-log-and-send-mail': {
        'task': 'app.tasks.send_log_email',
        'schedule': crontab(minute='*/3'),
    },
}

