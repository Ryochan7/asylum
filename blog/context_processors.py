from blog.conf import settings

def paginate_setting (request):
    return {"paginate_by": settings.PAGINATE_BY, "ANALYTICS": settings.site_settings.ANALYTICS}

