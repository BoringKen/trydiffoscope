from django import forms
from django.db import transaction

from .tasks import execute_diffoscope
from .models import Comparison

class CompareForm(forms.ModelForm):
    class Meta:
        model = Comparison
        fields = (
            'file_a',
            'file_b',
        )

    def save(self):
        instance = super(CompareForm, self).save()

        transaction.on_commit(lambda: execute_diffoscope.delay(instance.slug))

        return instance
