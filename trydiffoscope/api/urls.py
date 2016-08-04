from django.conf.urls import url

from . import views

urlpatterns = (
    url(r'^api/v2/comparison$', views.compare,
        name='compare'),
    url(r'^api/v2/comparison/(?P<slug>\w{12})$', views.comparison,
        name='comparison'),
)
