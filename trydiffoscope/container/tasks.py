import celery

from .utils import build_container, clean_images, clean_containers

@celery.task()
def update_container():
    build_container(force=True)

@celery.task()
def cleanup():
    clean_images()
    clean_containers()
