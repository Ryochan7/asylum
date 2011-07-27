from django import forms
from markitup.widgets import MarkItUpWidget
from projects.models import Project

class ProjectAdminForm (forms.ModelForm):
    class Meta (object):
        model = Project
        widgets = {
            "description": MarkItUpWidget (markitup_set="markitup/sets/default"),
        }

