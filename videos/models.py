import re
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from mezzanine.core.fields import FileField
from mezzanine.pages.models import Page
from mezzanine.core.models import Displayable, RichText, Slugged
from mezzanine.utils.models import AdminThumbMixin, upload_to

video_id_re = re.compile (r"http://(?:www\.)?youtube\.com/watch\?v=(\S+)(&)?.*")
blip_id_re = re.compile (r"http://(?:www\.)?blip.tv/\S+/.*-(\d+)")

class VideoCategory(Slugged):
    summary = models.CharField(max_length=200)
    description = models.TextField()

    class Meta(object):
        verbose_name_plural = "Video Categories"

    @models.permalink
    def get_absolute_url(self):
        return ("videos_category", (), {"slug": self.slug})


class Video(Displayable, RichText, AdminThumbMixin):
    featured_image = FileField(verbose_name=_("Featured Image"),
        upload_to=upload_to("videos.Video.featured_image", "uploads/video_images/%Y%m"),
        format="Image", max_length=255)#, null=True, blank=True)
    category = models.ForeignKey(VideoCategory)
    video_url = models.URLField(verbose_name=_("Video URL"), verify_exists=False,
        max_length=256)
    allow_comments = models.BooleanField(verbose_name=_("Allow comments"),
        default=True)

    admin_thumb_field = "featured_image"

    class Meta(object):
        ordering = ("-publish_date",)

    @models.permalink
    def get_absolute_url(self):
        return ('videos_detail', (), {'slug': self.slug})

    def meta_embed_url(self):
	embed_url = ""
	match = video_id_re.match (self.video_url)
	if match:
	    embed_url = "http://www.youtube.com/v/{0}?version=3&autohide=1"
	    embed_url = embed_url.format(match.group(1))

	return embed_url

    def embed_code(self):
        template = ""
        match = video_id_re.match (self.video_url)
        if match:
            template = "videos/youtube_embed.html"
            return render_to_string (template,
                {"video": self, "alias": match.group (1)})

        match = blip_id_re.match (self.video_url)
        if match:
            template = "videos/blip_embed.html"
            return render_to_string (template,
                {"video": self,
                 "alias": "http://blip.tv/rss/flash/{0}".format (match.group (1)),
                })

        return ""

    def next_video(self):
        next = None
        try:
            next = self.get_next_by_publish_date ()
        except self.__class__.DoesNotExist:
            return None

        return next

    def previous_video(self):
        previous = None
        try:
            previous = self.get_previous_by_publish_date ()
        except self.__class__.DoesNotExist:
            return None

        return previous


Video._meta.get_field("publish_date").db_index = True
Video._meta.get_field("slug").db_index = True

