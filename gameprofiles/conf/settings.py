from django.conf import settings as site_settings

APPLICATION_PAGINATE_BY = getattr (site_settings, "APPLICATION_PAGINATE_BY", 4)

