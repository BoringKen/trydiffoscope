from django.conf.urls import url

from . import views

urlpatterns = (
    url(r'^api/v3/comparison$', views.compare,
        name='compare'),
    url(r'^api/v3/comparison/(?P<slug>\w{12})$', views.comparison,
        name='comparison'),
)
