from django.contrib import admin
from markitup.widgets import MarkItUpWidget
from blog.models import Post

class PostAdmin (admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'pub_date', 'edit_date', 'published',)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ['title', 'body_raw']
    list_filter = ('pub_date', 'published')

admin.site.register (Post, PostAdmin)

