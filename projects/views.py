from django.views.generic import (TemplateView, ListView, DetailView,
    FormView, CreateView)
from django.shortcuts import get_object_or_404

from asylum_custom.views import CustomMezListView

from .models import Project, ProjectCategory
from .conf import settings

class IndexView (CustomMezListView):
    model = Project
    template_name = "projects/index.html"
    paginate_by = settings.PAGINATE_BY
    max_paging_links = 10
    queryset = Project.objects.select_related()

    def get_context_data (self, **kwargs):
	context = super(IndexView, self).get_context_data(**kwargs)
	context["project_categories"] = ProjectCategory.objects.all()
	return context

class DetailsView (DetailView):
    model = Project
    template_name = "projects/details.html"

    def get_context_data (self, **kwargs):
        context = super (DetailsView, self).get_context_data (**kwargs)
        context["editable_obj"] = context["project"]
        return context

