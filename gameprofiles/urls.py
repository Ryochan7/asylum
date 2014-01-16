from django.conf.urls import patterns, url
from .views import (IndexView, ApplicationDetailView, ProfileDownloadView)

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view (), name='profiles_index'),
    url(r'^app/(?P<slug>\S+)/$', ApplicationDetailView.as_view (), name='profiles_details'),
    url(r'^profile/download/(?P<id>\d+)/$', ProfileDownloadView.as_view(), name="profiles_download"),
)

