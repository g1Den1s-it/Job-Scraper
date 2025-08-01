from fastapi import FastAPI
from celery import Celery

from sqladmin import Admin, ModelView

from src.scraper.models import Job, Tag
from src.database import get_engine


app = FastAPI()

admin = Admin(app, get_engine())


class JobAdmin(ModelView, model=Job):
    column_list = [
        Job.id, Job.source, Job.url, Job.title,
        Job.content, Job.remote, Job.company,
        Job.time, Job.salery, Job.eng_level,
        Job.published_at, Job.company_link,Job.tags
    ]

class TagAdmin(ModelView, model=Tag):
    column_list = [
        Tag.id, Tag.name, Tag.jobs
    ]

admin.add_view(JobAdmin)
admin.add_view(TagAdmin)

