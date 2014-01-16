from django import template

from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import InclusionTag

from gameprofiles.models import Profile

register = template.Library()

class AlternativeProfiles(InclusionTag):
    name = "alternateprofiles"
    template = "gameprofiles/alternativeprofiles.html"

    def get_context(self, context):
        if "current_profile" in context:
            alternative_profiles = Profile.objects.exclude(
            id__in=context["current_profile"].id)
        else:
            alternative_profiles = []

        return {
            "profiles": alternative_profiles,
            "STATIC_URL": context["STATIC_URL"],
            "MEDIA_URL": context["MEDIA_URL"],
        }

register.tag(AlternativeProfiles)

