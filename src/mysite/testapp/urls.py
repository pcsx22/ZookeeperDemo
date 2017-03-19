from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^read/(?P<id>[0-9]+)/$',views.read,name='read'),
    url(r'^update/(?P<id>[0-9]+)/(?P<value>[a-zA-Z]+)$',views.update,name='update'),
]
