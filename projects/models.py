from django.db import models
from django.core import urlresolvers
import datetime

class ProjectType (models.Model):
    name = models.CharField (max_length=100)
    slug = models.SlugField (max_length=50, unique=True)
    summary = models.CharField (max_length=200)
    description = models.TextField ()

    def __unicode__ (self):
        return self.name

class Project (models.Model):
    title = models.CharField (max_length=100)
    slug = models.SlugField (max_length=50, unique=True)
    url = models.URLField (verify_exists=False)
    ptype = models.ForeignKey (ProjectType)
    begin_date = models.DateField ()
    end_date = models.DateField (blank=True)
    picture = models.ImageField (upload_to="project_images", max_length=512)
    summary = models.CharField (max_length=200)
    description = models.TextField ()

    class Meta (object):
        ordering = ('-end_date', "-begin_date",)

    def __unicode__ (self):
        return self.title

    def save (self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.begin_date

        super (Project, self).save (*args, **kwargs)

    @property
    def ongoing_project (self):
        ongoing = False
        if self.begin_date == self.end_date:
            ongoing = True

        return ongoing

    @property
    def dev_dates (self):
        date_str = ""
        if self.begin_date != self.end_date:
            date_str = "{0} - {1}".format (self.begin_date.strftime ("%B %Y"),
                self.end_date.strftime ("%B %Y"))
        else:
            date_str = "{0} - Present".format (self.begin_date.strftime ("%B %Y"))

        return date_str

    @models.permalink
    def get_absolute_url (self):
        return ("projects_details", (), {"slug": self.slug})

    @property
    def edit_link (self):
        url = urlresolvers.reverse ("admin:projects_project_change",
            args=(self.id,))
        return url

