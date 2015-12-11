import celery

from .utils import build_container

@celery.task()
def update_container():
    build_container(force=True)
