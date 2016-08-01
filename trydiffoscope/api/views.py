from django.shortcuts import resolve_url
from django.views.decorators.http import require_POST

from trydiffoscope.compare.forms import CompareForm

from .decorators import api_method

@api_method()
@require_POST
def compare(request):
    form = CompareForm(request.POST, request.FILES)

    if not form.is_valid():
        return 400, {
            'errors': form.errors,
        }

    instance = form.save()

    return 201, {
        'url': request.build_absolute_uri(instance.get_absolute_url()),
    }
