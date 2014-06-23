from linaro_django_pagination.middleware import PaginationMiddleware, get_page

class CustomPaginationMiddleware(PaginationMiddleware):
    """
    Insert get_page function into a different variable than request.page.
    Avoids conflict caused by mezzanine.pages.context_processors.page.
    """
    def process_request(self, request):
        request.__class__.page_num = get_page

