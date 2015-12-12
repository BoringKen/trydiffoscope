import celery
import datetime

from django.conf import settings

from ..models import Comparison

@celery.task()
def purge():
    epoch = datetime.datetime.utcnow() - datetime.timedelta(
        days=settings.TRYDIFFOSCOPE_RESULTS_RETENTION_DAYS,
    )

    for x in Comparison.objects.filter(updated__lte=epoch):
        x.delete()
