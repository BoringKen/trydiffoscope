from django.conf.urls import url

from . import views

urlpatterns = (
    url(r'^$', views.view,
        name='view'),
    url(r'^(?P<slug>\w{12})$', views.poll,
        name='poll'),
    url(r'^(?P<slug>\w{12})\.(?P<extension>html|txt)$', views.output,
        name='output'),
)
