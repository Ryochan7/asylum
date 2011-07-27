from django.conf.urls.defaults import *
from videos.views import IndexView, VideoDetailView

urlpatterns = patterns('',
    url (r'^$', IndexView.as_view (), name='videos_index'),
    url (r'^(?P<slug>\S+)/$', VideoDetailView.as_view (), name="videos_detail"),
)

