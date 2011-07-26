from django.contrib import admin
from videos.models import Video
from videos.forms import VideoAdminForm

class VideoAdmin (admin.ModelAdmin):
    form = VideoAdminForm
    prepopulated_fields = {"slug": ("title",)}

admin.site.register (Video, VideoAdmin)

