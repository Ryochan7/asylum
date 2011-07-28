from django import template
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings as site_settings
import math
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

@register.inclusion_tag ("videos/adjacent_list.html")
def adjacent_videos (video):
    STATIC_URL = site_settings.STATIC_URL
    paginate_by = settings.ADJACENT_PAGINATE_BY
    video_list = Video.objects.all ()
    placement_count = Video.objects.filter (pub_date__gte=video.pub_date).count ()
    paginator = Paginator (video_list, paginate_by)
    page = divmod (placement_count, paginate_by)
    page = int (page[0] + math.ceil (page[1] / float (paginate_by)))
    try:
        video_page = paginator.page (page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        video_page = paginator.page (1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        video_page = paginator.page (paginator.num_pages)

    return {
        "paginator": paginator,
        "page_obj": video_page,
        "object_list": video_page.object_list,
        "video_list": video_page.object_list,
        "is_paginated": video_page.has_other_pages (),
        "active_video": video,
        "STATIC_URL": STATIC_URL,
    }

