from django.contrib.syndication.feeds import Feed
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from taggit.models import Tag
from blog.models import Post
from blog.conf import settings

class LatestEntries (Feed):
    title = "Ryochan's Asylum"
    description = "Random Ranting from a Nobody"
    description_template = 'blog/feeds/latest_description.html'

    def link (self):
        return reverse ("blog_home_view")

    def items (self):
        return Post.published_objects.all ()[:settings.PAGINATE_BY]


class LatestEntriesByTag (Feed):
    description_template = 'blog/feeds/latest_description.html'
	
    def get_object (self, bits):
        if len (bits) != 1:
            raise ObjectDoesNotExist
        return Tag.objects.get (name=bits[0])

    def title (self, obj):
        return "Tag: %s | Ryochan's Asylum" % obj.name

    def link (self, obj):
        return reverse ("blog_tag_view", args=[obj.name])

    def description (self, obj):
        return "Recent posts tagged %s" % obj.name

    def items (self, obj):
        return Post.objects.filter (tags__name__in=[obj]).filter (published=True)[:settings.PAGINATE_BY]

