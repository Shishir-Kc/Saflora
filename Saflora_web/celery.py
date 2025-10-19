import os 
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE','Saflora_web.settings')
app = Celery('Saflora_web')

app.config_from_object('django.conf:settings',namespace='CELERY')

app.autodiscover_tasks()

@app.task(blind=True,ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
