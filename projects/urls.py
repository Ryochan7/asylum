from django.conf.urls import patterns, url
from .views import (IndexView, DetailsView)

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view (), name='projects_index'),
    url(r'^(?P<slug>\S+)/$', DetailsView.as_view (), name='projects_details'),
)

