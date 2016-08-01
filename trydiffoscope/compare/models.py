import os
import datetime
import functools

from django.db import models
from django.shortcuts import resolve_url
from django.utils.crypto import get_random_string

from .enums import StateEnum

def upload_to(instance, filename, prefix=''):
    return os.path.join(instance.slug, prefix, filename)

class Comparison(models.Model):
    file_a = models.FileField(
        upload_to=functools.partial(upload_to, prefix='a'),
    )

    file_b = models.FileField(
        upload_to=functools.partial(upload_to, prefix='b'),
    )

    state = models.IntegerField(
        choices=[(x.name, x.value) for x in StateEnum],
        default=StateEnum.queued.value,
    )

    output = models.TextField()

    slug = models.CharField(
        unique=True,
        max_length=12,
        default=functools.partial(get_random_string, 12, 'abcdefghkpqrstuvxyz'),
    )

    created = models.DateTimeField(default=datetime.datetime.utcnow)
    updated = models.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        ordering = ('-created',)
        get_latest_by = 'created'

    def __unicode__(self):
        return u"slug=%s state=%s a=%s b=%s" % (
            self.slug,
            self.state,
            self.file_a.name,
            self.file_b.name,
        )

    def get_state_enum(self):
        return {x.value: x for x in StateEnum}[self.state]

    def get_absolute_url(self):
        return resolve_url('compare:poll', self.slug)
