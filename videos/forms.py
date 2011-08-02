import re
import logging
from django import forms
from markitup.widgets import MarkItUpWidget
from videos.models import Video

logger = logging.getLogger ("videos.forms")

class VideoAdminForm (forms.ModelForm):
    class Meta (object):
        model = Video
        widgets = {
            "description": MarkItUpWidget (markitup_set="markitup/sets/default"),
        }

    def clean (self):
        if self.cleaned_data["summary"] == "":
            if len (self.cleaned_data["description"]) > 200:
                self.cleaned_data["summary"] = "{0}...".format (
                    self.cleaned_data["description"][:197])
            else:
                self.cleaned_data["summary"] = self.cleaned_data["description"]

        return self.cleaned_data

class VideoOptions (forms.Form):
    autoplay = forms.BooleanField (initial=False)

