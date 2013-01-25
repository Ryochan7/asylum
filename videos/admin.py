from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from mezzanine.core.admin import DisplayableAdmin

from .models import Video, VideoCategory

video_fieldsets = deepcopy(DisplayableAdmin.fieldsets)
video_fieldsets[0][1]["fields"].extend(["featured_image", "category", "video_url", "content", "allow_comments"])

video_list_display = list(DisplayableAdmin.list_display)
video_list_display.insert(0, "admin_thumb")

class VideoCategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": ["title", "summary", "description"]
        }),
        (_("Optional"), {
            "fields": ["slug"],
            "classes": ("collapse-closed",),
        }),
    )
    list_display = ("title", "summary",)


class VideoAdmin(DisplayableAdmin):
    fieldsets = video_fieldsets
    list_display = video_list_display


admin.site.register(Video, VideoAdmin)
admin.site.register(VideoCategory, VideoCategoryAdmin)

