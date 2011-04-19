from django.conf import settings as site_settings

PAGINATE_BY = getattr (site_settings, "PAGINATE_BY", 10)
COMMENT_DAYS_OPEN = getattr (site_settings, "COMMENT_DAYS_OPEN", 60)

