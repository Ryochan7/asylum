from django.views.generic import ListView

class CustomMezListView(ListView):
    max_paging_links = None

    def get_max_paging_links(self):
	max_paging_links = None
	if self.max_paging_links is not None:
	    max_paging_links = self.max_paging_links
	else:
	    max_paging_links = 0

	return max_paging_links

    def paginate_queryset(self, queryset, page_size):
	(paginator, page, queryset, is_paginated) = super(CustomMezListView, self).paginate_queryset(queryset, page_size)

	page_range = paginator.page_range
	max_paging_links = self.get_max_paging_links()
	if max_paging_links > 0 and (paginator.num_pages > max_paging_links):
	    start = min(paginator.num_pages - max_paging_links,
		max(0, page.number - (max_paging_links / 2) - 1))

	    page_range = page_range[start:start + max_paging_links]

	page.visible_page_range = page_range
	return (paginator, page, queryset, is_paginated)

