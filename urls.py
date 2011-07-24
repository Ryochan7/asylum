from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns ('',
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url (r'^$', 'blog.views.home_view', name='home_view'),
    url (r'^blog/', include ('blog.urls')),
    url (r'^about/', 'django.views.generic.simple.direct_to_template', {"template": "about.html"}, name="about_view"),
    url (r'^projects/', 'django.views.generic.simple.direct_to_template', {"template": "projects.html"}, name="projects_view"),
)


if settings.DEBUG:
    urlpatterns += patterns ('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

