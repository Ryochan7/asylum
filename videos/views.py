import logging
import time
from django.views.generic import (TemplateView, ListView, DetailView,
    FormView, CreateView)
from django.shortcuts import get_object_or_404
from videos.models import Video
from videos.conf import settings

logger = logging.getLogger ("videos.views")

class IndexView (ListView):
    model = Video
    template_name = "videos/index.html"
    ajax_template_name = "videos/list_display.html"
    paginate_by = settings.PAGINATE_BY

    def get_template_names (self):
        if self.request.is_ajax ():
            return [self.ajax_template_name]

        return super (IndexView, self).get_template_names ()

class VideoDetailView (DetailView):
    model = Video
    template_name = "videos/detail.html"


