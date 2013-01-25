import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.fields import FileField
from mezzanine.pages.models import Page
from mezzanine.core.models import Displayable, RichText, Slugged
from mezzanine.utils.models import AdminThumbMixin, upload_to

class ProjectCategory(Slugged):
    summary = models.CharField(max_length=200)
    description = models.TextField()

    class Meta(object):
        verbose_name_plural = "Project Categories"


class Project(Displayable, RichText, AdminThumbMixin):
    featured_image = FileField(verbose_name=_("Featured Image"),
        upload_to=upload_to("projects.Project.featured_image", "uploads/project_images/%Y%m"),
        format="Image", max_length=255)
    #allow_comments = models.BooleanField(verbose_name=_("Allow comments"),
    #    default=True)
    ongoing = models.BooleanField(verbose_name=_("Ongoing Project"),
        default=True)
    url = models.URLField(verbose_name=_("Project URL"),
        verify_exists=False)
    category = models.ForeignKey(ProjectCategory)
    begin_date = models.DateField(verbose_name=_("Project Start Date"))
    end_date = models.DateField(verbose_name=_("Project End Date"))
    summary = models.CharField(max_length=200)    

    admin_thumb_field = "featured_image"

    class Meta(object):
        ordering = ("-end_date", "-begin_date",)

    @models.permalink
    def get_absolute_url(self):
        return ("projects_details", (), {"slug": self.slug})

    @property
    def ongoing_project (self):
	return self.ongoing

    @property
    def dev_dates (self):
        date_str = ""
        if not self.ongoing:
            date_str = "{0} - {1}".format (self.begin_date.strftime ("%B %Y"),
                self.end_date.strftime ("%B %Y"))
        else:
            date_str = "{0} - Present".format (self.begin_date.strftime ("%B %Y"))

        return date_str

Project._meta.get_field("publish_date").db_index = True
Project._meta.get_field("slug").db_index = True

