import json
import functools

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache

class api_method(object):
    def __call__(self, fn):
        @csrf_exempt
        @never_cache
        @functools.wraps(fn)
        def wrapped(request, *args, **kwargs):
            response = fn(request, *args, **kwargs)

            try:
                status, data = response
            except ValueError:
                return response

            body = json.dumps({
                'result': data,
                'status': status
            }, indent=2)

            return HttpResponse(
                body,
                status=status,
                content_type='application/json',
            )
        return wrapped
