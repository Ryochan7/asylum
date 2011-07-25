from django.views.generic import (TemplateView, ListView, DetailView,
    FormView, CreateView)
from django.shortcuts import get_object_or_404
from projects.models import Project, ProjectType
from projects.conf import settings

class IndexView (ListView):
    model = Project
    template_name = "projects/index.html"
    paginate_by = settings.PAGINATE_BY

class DetailsView (DetailView):
    model = Project
    template_name = "projects/details.html"

