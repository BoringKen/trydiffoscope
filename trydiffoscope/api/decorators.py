import json
import functools

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

class api_method(object):
    def __call__(self, fn):
        @csrf_exempt
        @functools.wraps(fn)
        def wrapped(request, *args, **kwargs):
            response = fn(request, *args, **kwargs)

            try:
                status, data = response
            except ValueError:
                return response

            return HttpResponse(
                json.dumps(data),
                status=status,
                content_type='application/json',
            )
        return wrapped