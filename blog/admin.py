from django.contrib import admin
from blog.models import Post


class PostAdmin (admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'pub_date', 'edit_date', 'published',)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ['title', 'body_raw']
    list_filter = ('pub_date', 'published')

    class Media (object):
        js = ('js/wmd-textareas.js', 'wmd/wmd.js',)

admin.site.register (Post, PostAdmin)


