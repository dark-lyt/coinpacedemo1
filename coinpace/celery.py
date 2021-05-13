from __future__ import absolute_import, unicode_literals
import os 
from celery import Celery 



# Set default Django settings 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coinpace.settings') 
app = Celery('coinpace') 

# Celery will apply all configuration keys with defined namespace 
app.config_from_object('django.conf:settings', namespace='CELERY')  

# Load tasks from all registered apps 
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
