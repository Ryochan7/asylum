from blog.conf import settings

def paginate_setting (request):
    return {
        "paginate_by": settings.PAGINATE_BY,
        "ANALYTICS": settings.site_settings.ANALYTICS,
        "DISQUS_SHORTNAME": settings.DISQUS_SHORTNAME,
        "DISQUS_DEVELOPER": settings.DISQUS_DEVELOPER,
    }

