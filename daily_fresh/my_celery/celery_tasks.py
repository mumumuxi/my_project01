from celery import Celery
from django.core.mail import send_mail

# 为celery配置django环境
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "daily_fresh.settings")
django.setup()

# celery -A my_celery.celery_tasks worker -l info

app = Celery('my_celery.celery_tasks', broker='redis://localhost:6379/2')

@app.task
def tasks_send_mail(subject,message,sender,receiver,html_message):
    print('begin...')
    import time
    time.sleep(10)
    send_mail(subject, message, sender, receiver, html_message=html_message)
    print('end...')

