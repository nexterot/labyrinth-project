from django.conf.urls import url
from .views import index, registration, logout, info

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^registration/$', registration, name='registration'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^info/$', info, name='info')
]
