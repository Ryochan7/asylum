from django.contrib import admin
from blog.models import Post


class PostAdmin (admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'pub_date', 'edit_date', 'published',)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ['title', 'body_raw']
    list_filter = ('pub_date', 'published')

    class Media (object):
        js = (
            "wymeditor/jquery/jquery.js",
            "wymeditor/wymeditor/jquery.wymeditor.js",
            "js/admin_textarea.js",
        )

admin.site.register (Post, PostAdmin)

