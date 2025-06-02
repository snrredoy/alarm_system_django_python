from celery import shared_task
from celery.schedules import crontab

@shared_task
def alarm_task():
    print("Alarm!")
