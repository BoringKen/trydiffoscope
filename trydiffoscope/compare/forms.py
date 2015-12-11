from django import forms

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

        execute_diffoscope.delay(instance.slug)

        return instance
