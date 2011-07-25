from django.conf import settings as site_settings

PAGINATE_BY = getattr (site_settings, "PROJECTS_PAGINATE_BY", 10)

