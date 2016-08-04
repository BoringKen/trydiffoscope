from django.shortcuts import resolve_url

def resolve_absolute_url(request, *args, **kwargs):
    return request.build_absolute_uri(resolve_url(*args, **kwargs))
