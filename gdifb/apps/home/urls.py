from django.conf.urls.defaults import patterns, url
from .views import MainView

urlpatterns = patterns('',
    url('^$', MainView.as_view(), name="main"),
)

