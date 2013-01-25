from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
#from mezzanine.pages.admin import PageAdmin
from mezzanine.core.admin import DisplayableAdmin

from .models import Project, ProjectCategory

project_fieldsets = deepcopy(DisplayableAdmin.fieldsets)
project_fieldsets[0][1]["fields"].extend([("begin_date", "end_date"), "ongoing", "featured_image", "category", "content"])

project_list_display = list(DisplayableAdmin.list_display)
project_list_display.insert(0, "admin_thumb")

class ProjectAdmin(DisplayableAdmin):
    #form = ProjectForm

    fieldsets = project_fieldsets
    list_display = project_list_display

class ProjectCategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": ["title", "summary", "description"]
        }),
        (_("Optional"), {
            "fields": ["slug"],
            "classes": ("collapse-closed",),
        }),
    )
    list_display = ("title", "summary",)


admin.site.register (ProjectCategory, ProjectCategoryAdmin)
admin.site.register (Project, ProjectAdmin)

