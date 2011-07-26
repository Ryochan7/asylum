from django import template
from django.conf import settings as site_settings
from videos.models import Video
from videos.conf import settings

register = template.Library()

@register.inclusion_tag ("videos/featured.html")
def latest_videos ():
    num = settings.FEATURED_NUMBER
    STATIC_URL = site_settings.STATIC_URL
    latest_video_list = Video.objects.all ()[:num]
    return {
        "latest_video_list": latest_video_list,
        "STATIC_URL": STATIC_URL,
    }

