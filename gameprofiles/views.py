from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from asylum_custom.views import CustomMezListView, get_client_ip

from .models import (Application, FeaturedProfile, Profile,
    ProfileDownload)
from .conf import settings

class IndexView(CustomMezListView):
    queryset = Application.objects.order_by("slug")
    template_name = "gameprofiles/index.html"
    paginate_by = 10
    max_paging_links = 5


class ApplicationDetailView(DetailView):
    model = Application
    template_name = "gameprofiles/details.html"

    def get_context_data(self, **kwargs):
        context = super(ApplicationDetailView, self).get_context_data(**kwargs)
        context["featured_profile"] = FeaturedProfile.objects.filter(application__slug=self.kwargs["slug"]).select_related().first()
        context["all_profiles"] = Profile.objects.filter(application__slug=self.kwargs["slug"]).select_related()
        context["all_profiles_count"] = Profile.objects.filter(application__slug=self.kwargs["slug"]).count()
        context["editable_obj"] = context["application"]
        return context


class ProfileDownloadView(View):
    def get(self, request, *args, **kwargs):
        current_profile = get_object_or_404(Profile, id=self.kwargs["id"])
        ProfileDownload.objects.get_or_create(ipaddress=get_client_ip(request), profile=current_profile)
        return redirect(current_profile.file.url)

