from django.views.generic import ListView
from mezzanine.utils.views import paginate

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class CustomMezListView(ListView):
    max_paging_links = 0
    page_kwarg = "page"

    def get_max_paging_links(self):
	return self.max_paging_links

    def paginate_queryset(self, queryset, page_size):
        page_kwarg = self.page_kwarg
        page_num = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        page = paginate(queryset, page_num, page_size,
            self.get_max_paging_links())
        return (page.paginator, page, page.object_list, page.has_other_pages())

