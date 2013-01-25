import datetime

from django import forms

from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta(object):
        model = Project

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        if "initial" not in kwargs or not kwargs["initial"]:
            self.fields["publish_date"].initial = datetime.datetime.now
 
