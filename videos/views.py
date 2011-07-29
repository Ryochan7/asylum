import logging
import time
from django.views.generic import (TemplateView, ListView, DetailView,
    FormView, CreateView)
from django.shortcuts import get_object_or_404
from videos.models import Video, VideoCategory
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

    def get_context_data (self, **kwargs):
        context = super (IndexView, self).get_context_data (**kwargs)
        context["category_list"] =  VideoCategory.objects.all ().order_by ("title")
        return context

class VideoDetailView (DetailView):
    model = Video
    template_name = "videos/detail.html"

class AjaxAdjacentView (ListView):
    model = Video
    template_name="videos/adjacent_list.html"
    paginate_by = settings.ADJACENT_PAGINATE_BY

    def get_queryset (self):
        return Video.objects.filter (category__slug=self.kwargs["cat_slug"])

    def get_context_data (self, **kwargs):
        context = super (AjaxAdjacentView, self).get_context_data (**kwargs)
        context["active_video"] = get_object_or_404 (Video, id=self.kwargs["id"])
        return context

class CategoryView (IndexView):
    template_name = "videos/category.html"

    def get_queryset (self):
        return Video.objects.filter (category__slug=self.kwargs["slug"])

    def get_context_data (self, **kwargs):
        context = super (CategoryView, self).get_context_data (**kwargs)
        context["category"] = get_object_or_404 (VideoCategory, slug=self.kwargs["slug"])
        return context

