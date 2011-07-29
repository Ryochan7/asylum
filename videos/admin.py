from django.contrib import admin
from videos.models import Video, VideoCategory
from videos.forms import VideoAdminForm

class VideoCategoryAdmin (admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

class VideoAdmin (admin.ModelAdmin):
    form = VideoAdminForm
    prepopulated_fields = {"slug": ("title",)}

admin.site.register (VideoCategory, VideoCategoryAdmin)
admin.site.register (Video, VideoAdmin)

