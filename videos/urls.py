from django.conf.urls.defaults import *
from videos.views import IndexView, VideoDetailView, AjaxAdjacentView

urlpatterns = patterns('',
    url (r'^$', IndexView.as_view (), name='videos_index'),
    url (r'^(?P<slug>[\w-]+)/$', VideoDetailView.as_view (), name="videos_detail"),
    url (r'^adjacent/(?P<id>\d+)/page/(?P<page>\d+)/$', AjaxAdjacentView.as_view (), name="videos_adjacent"),
)

