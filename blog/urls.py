from django.conf.urls.defaults import *
from blog.feeds import LatestEntries, LatestEntriesByTag

feeds = {
	'latest': LatestEntries,
	'tag': LatestEntriesByTag,
}

urlpatterns = patterns('',
    url (r'^$', 'blog.views.blog_home_view', name='blog_home_view'),
    url (r'^search/$', 'blog.views.search_view', name='blog_search_view'),
    url (r'^preview/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{2})/(?P<slug>\S+)/$', 'blog.views.post_preview_view', name='blog_post_preview_view'),
    url (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{2})/(?P<slug>\S+)/$', 'blog.views.post_detail_view', name='blog_post_detail_view'),
    url (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', 'blog.views.month_view', name='blog_month_view'),
    url (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', 'blog.views.day_view', name='blog_day_view'),
    url (r'^tag/(?P<tag>\S+)/$', 'blog.views.tag_view', name='blog_tag_view'),
    url (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}, name='blog_feeds_view'),
)

