from django.conf.urls import url

from . import views

app_name = 'rate'
urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^index/$', views.IndexView.as_view(), name='index'),
]
