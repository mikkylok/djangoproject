from . import views
from django.conf.urls import include, url

urlpatterns = [
    url('', views.index, name='index'),
    url(r'search', views.search, name='search'),
]
