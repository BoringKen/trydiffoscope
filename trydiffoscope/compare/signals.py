import shutil

from django.db import models
from django.dispatch import receiver
from django.core.files.storage import default_storage

from .models import Comparison

@receiver(models.signals.post_delete, sender=Comparison)
def post_delete_comparison(sender, instance, *args, **kwargs):
    shutil.rmtree(default_storage.path(instance.slug), ignore_errors=True)
