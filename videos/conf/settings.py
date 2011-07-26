from django.conf import settings as site_settings

PAGINATE_BY = getattr (site_settings, "VIDEO_PAGINATE_BY", 4)
FEATURED_NUMBER = getattr (site_settings, "VIDEO_FEATURED_NUMBER", 5)

