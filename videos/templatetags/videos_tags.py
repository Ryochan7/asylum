import math

from django import template
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import InclusionTag

from videos.models import Video, VideoCategory
from videos.conf import settings

register = template.Library()

@register.inclusion_tag ("videos/featured.html", takes_context=True)
def latest_videos (context):
    num = settings.FEATURED_NUMBER
    latest_video_list = Video.objects.all ()[:num]
    return {
        "latest_video_list": latest_video_list,
	"STATIC_URL": context["STATIC_URL"],
	"MEDIA_URL": context["MEDIA_URL"],
    }

@register.inclusion_tag ("videos/adjacent_list.html", takes_context=True)
def adjacent_videos (context, video):
    paginate_by = settings.ADJACENT_PAGINATE_BY
    video_list = Video.objects.filter (category=video.category)
    placement_count = Video.objects.filter (category=video.category).filter (publish_date__gte=video.publish_date).count ()
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
	"STATIC_URL": context["STATIC_URL"],
	"MEDIA_URL": context["MEDIA_URL"],
    }

class VideoCategoriesTag(InclusionTag):
    name="video_categories_block"
    template = "videos/category_include.html"

    def get_context(self, context):
	categories = VideoCategory.objects.order_by("title")
	return {
	    "category_list": categories,
	    "STATIC_URL": context["STATIC_URL"],
	    "MEDIA_URL": context["MEDIA_URL"],
	}

register.tag(VideoCategoriesTag)

