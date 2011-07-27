from django.contrib import admin
from projects.models import Project, ProjectType
from projects.forms import ProjectAdminForm

class ProjectTypeAdmin (admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class ProjectAdmin (admin.ModelAdmin):
    form = ProjectAdminForm
    prepopulated_fields = {"slug": ("title",)}

#class PostAdmin (admin.ModelAdmin):
#    list_display = ('title', 'slug', 'author', 'pub_date', 'edit_date', 'published',)
#    prepopulated_fields = {"slug": ("title",)}
#    search_fields = ['title', 'body_raw']
#    list_filter = ('pub_date', 'published')

admin.site.register (ProjectType, ProjectTypeAdmin)
admin.site.register (Project, ProjectAdmin)

