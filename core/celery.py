import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")
# read celery config from settings.py using the CELERY_ prefix
app.config_from_object("django.conf:settings", namespace="CELERY")
# auto-discover tasks in installed apps
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "check-due-tasks-every-minute": {
        "task": "tasks.tasks.check_due_tasks",  # appname.filename.function
        "schedule": crontab(minute="*"),  # every 1 min
    },
}