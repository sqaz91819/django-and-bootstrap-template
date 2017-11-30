from django.conf.urls import url

from . import views

app_name = 'rate'
urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^index/$', views.IndexView.as_view(), name='index'),
    url(r'^forms/$', views.FormsView.as_view(), name='forms'),
    url(r'^modify/$', views.ModifyView.as_view(), name='modify'),
    url(r'^compare/$', views.CompareView.as_view(), name='compare'),
    url(r'^score/$', views.score, name='score'),
]
