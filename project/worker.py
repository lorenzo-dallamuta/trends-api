import os
from celery import Celery
from driver import list_topics

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get(
    "CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379")


@celery.task(name="create_query")
def create_query(**kwargs):
    topics = list_topics(**kwargs)
    return topics
