import datetime
import markdown
from django.db import models
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse
from tagging.fields import TagField
from tagging.models import Tag
from blog.conf import settings
if getattr (settings.site_settings, "PINGBACK_LINKS", False):
    from pingback.client import ping_external_links
if getattr (settings.site_settings, "DIRECTORY_URLS", None):
    from pingback.client import ping_directories
if getattr (settings.site_settings, "SPHINX_SERVER", None):
    from djangosphinx.models import SphinxSearch
from blog.managers import PublishedPostManager
from blog.utils.mdx_youtube import YouTubeEmbedExtension

class Post (models.Model):
    title = models.CharField (max_length=50)
    slug = models.SlugField (max_length=50, unique=True)
    body = models.TextField (editable=False, default=u"")
    body_raw = models.TextField ('Body', help_text=u"Enter the post using <a href='http://daringfireball.net/projects/markdown/syntax'>Markdown</a> syntax")
    pub_date = models.DateTimeField (default=datetime.datetime.now)
    edit_date = models.DateTimeField (default=datetime.datetime.now)
    enable_comments = models.BooleanField (default=False)
    published = models.BooleanField (default=False, help_text=u"Should the post be seen by the public")
    tags = TagField ()
    author = models.ForeignKey (User)
    comment_count = models.PositiveIntegerField (default=0, editable=False)
    comments = generic.GenericRelation (Comment, object_id_field="object_pk")

    objects = models.Manager ()
    published_objects = PublishedPostManager ()
    if getattr (settings.site_settings, "SPHINX_SERVER", None):
        search = SphinxSearch (mode="SPH_MATCH_EXTENDED")

    def __unicode__ (self):
        return self.title

    class Meta (object):
        ordering = ('-pub_date',)

    @models.permalink
    def get_absolute_url (self):
        year = self.pub_date.strftime ("%Y")
        month = self.pub_date.strftime ("%2m")
        day = self.pub_date.strftime ("%2d")
        if self.published:
            return ('blog_post_detail_view', (), {'year': year, 'month': month, 'day': day, 'slug': self.slug})
        else:
            return ('blog_post_preview_view', (), {'year': year, 'month': month, 'day': day, 'slug': self.slug})

    @property
    def edit_link (self):
        from django.contrib.contenttypes.models import ContentType
        from django.contrib import admin
        from django.core import urlresolvers
        ctype = ContentType.objects.get_for_model (Post)
        resolver = urlresolvers.RegexURLResolver(r'^/', settings.site_settings.ROOT_URLCONF)
        admin_url = resolver.reverse_dict[admin.site.root][1].strip ('(.*)')
        return "/{0}{1}/{2}/{3}/".format (admin_url, ctype.app_label,
                ctype.model, self.id)

    def save (self, *args, **kwargs):
        md = markdown.Markdown ()
        extension = YouTubeEmbedExtension ()
        extension.extendMarkdown (md)
        self.body = md.convert (self.body_raw).strip ()
        super (Post, self).save (*args, **kwargs)

    def delete (self, *args, **kwargs):
        Tag.objects.update_tags (self, "")
        super (Post, self).delete (*args, **kwargs)

    def comments_open (self):
        if self.enable_comments:
            return self.pub_date + datetime.timedelta (settings.COMMENT_DAYS_OPEN) >= datetime.datetime.now ()
        return False

    def get_previous_post (self):
        try:
            prev_post = self.get_previous_by_pub_date (published=True)
        except self.__class__.DoesNotExist:
            return False

        return prev_post

    def get_next_post (self):
        try:
            next_post = self.get_next_by_pub_date (published=True)
        except self.__class__.DoesNotExist:
            return False

        return next_post


if getattr (settings.site_settings, "PINGBACK_LINKS", False):
    models.signals.post_save.connect (ping_external_links (
            content_attr="body",
            filtr=lambda instance: instance.published == True,
            url_attr="get_absolute_url"),
        sender=Post, dispatch_uid="pingback_external_links",
        weak=False)

if getattr (settings.site_settings, "DIRECTORY_URLS", None):
    models.signals.post_save.connect (ping_directories (
            url_attr="get_absolute_url",
            filtr=lambda instance: instance.published == True,
            feed_url_fun=lambda instance: reverse ("blog_feeds_view",
            args=["latest"])),
        sender=Post, dispatch_uid="pingback_directories", weak=False)

