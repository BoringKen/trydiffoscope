from django.conf import settings
from django.conf.urls import include, url
from django.views.static import serve

urlpatterns = (
    url(r'', include('trydiffoscope.api.urls',
        namespace='api')),
    url(r'', include('trydiffoscope.compare.urls',
        namespace='compare')),
    url(r'', include('trydiffoscope.static.urls',
        namespace='static')),
)

if settings.DEBUG:
    urlpatterns += (
        url(r'^storage/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
