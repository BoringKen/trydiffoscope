import os

from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from trydiffoscope.compare.forms import CompareForm
from trydiffoscope.utils.shortcuts import resolve_absolute_url

from trydiffoscope.compare.models import Comparison

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
        'uri': resolve_absolute_url(request, 'api:comparison', instance.slug),
    }

@api_method()
def comparison(request, slug):
    instance = get_object_or_404(Comparison, slug=slug)

    response = {
        'uri': resolve_absolute_url(request, instance),
        'state': instance.get_state_enum().name,

        'files': {x: {
            'name': os.path.basename(getattr(instance, 'file_%s' % x).name),
            'size': getattr(instance, 'file_%s' % x).size,
        } for x in ('a', 'b')},

        'formats': {x: resolve_absolute_url(
            request, 'compare:output', instance.slug, y,
        ) for x, y in (('text', 'txt'), ('html', 'html'))},

        'created': instance.created,
        'updated': instance.updated,
    }

    return 200, response
