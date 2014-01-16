from django.views.generic import ListView
from mezzanine.utils.views import paginate

class CustomMezListView(ListView):
    max_paging_links = 0
    page_kwarg = "page"

    """def paginate_queryset(self, queryset, page_size):
	(paginator, page, queryset, is_paginated) = super(CustomMezListView, self).paginate_queryset(queryset, page_size)

	page_range = paginator.page_range
	max_paging_links = self.get_max_paging_links()
	if max_paging_links > 0 and (paginator.num_pages > max_paging_links):
	    start = min(paginator.num_pages - max_paging_links,
		max(0, page.number - (max_paging_links / 2) - 1))

	    page_range = page_range[start:start + max_paging_links]

	page.visible_page_range = page_range
	return (paginator, page, queryset, is_paginated)"""

    def get_max_paging_links(self):
	return self.max_paging_links

    def paginate_queryset(self, queryset, page_size):
        page_kwarg = self.page_kwarg
        page_num = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        page = paginate(queryset, page_num, page_size,
            self.get_max_paging_links())
        return (page.paginator, page, page.object_list, page.has_other_pages())

