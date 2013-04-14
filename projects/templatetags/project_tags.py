from django import template

from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import InclusionTag

from projects.models import Project

register = template.Library()

class LatestProject(InclusionTag):
    name = "latest_project"
    template = "projects/latest_video.html"

    def get_context(self, context):
	latest = Project.objects.order_by("-publish_date")[:1]
	return {
	    "latest_project": latest,
	    "STATIC_URL": context["STATIC_URL"],
	    "MEDIA_URL": context["MEDIA_URL"],
	}

register.tag(LatestProject)

