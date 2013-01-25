from django.conf.urls.defaults import *
from .views import (IndexView, VideoDetailView, CategoryView,
    AjaxAdjacentView)

urlpatterns = patterns('',
    url (r'^$', IndexView.as_view (), name='videos_index'),
    url (r'^category/(?P<slug>[\w-]+)/$', CategoryView.as_view (), name='videos_category'),
    url (r'^(?P<slug>[\w-]+)/$', VideoDetailView.as_view (), name="videos_detail"),
    url (r'^adjacent/(?P<cat_slug>[\w-]+)/(?P<id>\d+)/page/(?P<page>\d+)/$', AjaxAdjacentView.as_view (), name="videos_adjacent"),
)
 
