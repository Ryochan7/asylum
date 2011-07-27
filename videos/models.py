import re
import datetime
from django.db import models
from django.core import urlresolvers
from django.template.loader import render_to_string

video_id_re = re.compile (r"http://(?:www\.)?youtube\.com/watch\?v=(\S+)(&)?.*")
blip_id_re = re.compile (r"http://(?:www\.)?blip.tv/\S+/.*-(\d+)")

class Video (models.Model):
    title = models.CharField (max_length=200)
    slug = models.SlugField (max_length=50, unique=True)
    pub_date = models.DateTimeField (default=datetime.datetime.now, db_index=True)
    photo = models.ImageField (upload_to="video_images", max_length=512, blank=True)
    video_url = models.CharField (max_length=256)
    summary = models.CharField (max_length=200, blank=True, help_text=u"If summary is left blank, a truncated version of the description will be used")
    description = models.TextField ()

    def __unicode__ (self):
        return self.title

    @models.permalink
    def get_absolute_url (self):
        return ('videos_detail', (), {'slug': self.slug})

    def embed_code (self):
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

    @property
    def edit_link (self):
        url = urlresolvers.reverse ("admin:videos_video_change",
            args=(self.id,))
        return url

