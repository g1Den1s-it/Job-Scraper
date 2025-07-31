from celery import Celery
from celery.schedules import crontab

celery_app = Celery('app', broker="redis://redis:6379/0", backend="redis://redis:6379/1")


celery_app.conf.timezone = 'Europe/Kyiv'

celery_app.conf.update(task_track_started=True)
celery_app.conf.update(task_serializer='pickle')
celery_app.conf.update(result_serializer='pickle')
celery_app.conf.update(accept_content=['pickle', 'json'])
celery_app.conf.update(result_expires=200)
celery_app.conf.update(result_persistent=True)
celery_app.conf.update(worker_send_task_events=False)
celery_app.conf.update(worker_prefetch_multiplier=1)


celery_app.conf.beat_schedule = {
   'run-hourly-article-update': {
        'task': 'tasks.scrap_work',
        'schedule': crontab(hour=1),
    },   
}

celery_app.autodiscover_tasks(['src.scraper.tasks'], force=True)
