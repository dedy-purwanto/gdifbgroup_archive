from django.conf.urls.defaults import patterns, url
from posts.views import PostDetailView

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/$', PostDetailView.as_view(), name='detail'),
)
