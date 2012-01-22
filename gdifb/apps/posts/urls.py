from django.conf.urls.defaults import patterns, url
from posts.views import PostDetailView, PostListView

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/$', PostDetailView.as_view(), name='detail'),
    url(r'list/$', PostListView.as_view(), name='list'),
)
