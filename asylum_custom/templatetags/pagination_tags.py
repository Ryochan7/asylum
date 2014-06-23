from django.core.paginator import Paginator, InvalidPage
from django.template import (
    Context,
    Library,
    Node,
    TOKEN_BLOCK,
    TemplateSyntaxError,
    Variable,
)

from linaro_django_pagination.templatetags.pagination_tags import (
    AutoPaginateNode,
    do_paginate,
)


def do_autopaginate(parser, token):
    """
    Splits the arguments to the autopaginate tag and formats them correctly.

    Syntax is:

        autopaginate QUERYSET [PAGINATE_BY] [ORPHANS] [as NAME]
    """
    # Check whether there are any other autopaginations are later in this template
    expr = lambda obj: (obj.token_type == TOKEN_BLOCK and \
        len(obj.split_contents()) > 0 and obj.split_contents()[0] == "autopaginate")
    multiple_paginations = len(filter(expr, parser.tokens)) > 0

    i = iter(token.split_contents())
    paginate_by = None
    queryset_var = None
    context_var = None
    orphans = None
    word = None
    try:
        word = i.next()
        assert word == "autopaginate"
        queryset_var = i.next()
        word = i.next()
        if word != "as":
            paginate_by = word
            try:
                paginate_by = int(paginate_by)
            except ValueError:
                pass
            word = i.next()
        if word != "as":
            orphans = word
            try:
                orphans = int(orphans)
            except ValueError:
                pass
            word = i.next()
        assert word == "as"
        context_var = i.next()
    except StopIteration:
        pass
    if queryset_var is None:
        raise TemplateSyntaxError(
            "Invalid syntax. Proper usage of this tag is: "
            "{% autopaginate QUERYSET [PAGINATE_BY] [ORPHANS]"
            " [as CONTEXT_VAR_NAME] %}")
    return CustomAutoPaginateNode(queryset_var, multiple_paginations, paginate_by, orphans, context_var)


class CustomAutoPaginateNode(AutoPaginateNode):
    def render(self, context):
        if self.multiple_paginations or "paginator" in context:
            page_suffix = '_%s' % self.queryset_var
        else:
            page_suffix = ''

        key = self.queryset_var.var
        value = self.queryset_var.resolve(context)
        if isinstance(self.paginate_by, int):
            paginate_by = self.paginate_by
        else:
            paginate_by = self.paginate_by.resolve(context)
        if isinstance(self.orphans, int):
            orphans = self.orphans
        else:
            orphans = self.orphans.resolve(context)
        paginator = Paginator(value, paginate_by, orphans)
        try:
            request = context['request']
        except KeyError:
            raise ImproperlyConfigured(
                "You need to enable 'django.core.context_processors.request'."
                " See linaro-django-pagination/README file for TEMPLATE_CONTEXT_PROCESSORS details")
        try:
            page_obj = paginator.page(request.page_num(page_suffix))
        except InvalidPage:
            if INVALID_PAGE_RAISES_404:
                raise Http404('Invalid page requested.  If DEBUG were set to ' +
                    'False, an HTTP 404 page would have been shown instead.')
            context[key] = []
            context['invalid_page'] = True
            return u''
        if self.context_var is not None:
            context[self.context_var] = page_obj.object_list
        else:
            context[key] = page_obj.object_list
        context['paginator'] = paginator
        context['page_obj'] = page_obj
        context['page_suffix'] = page_suffix
        return u''

register = Library()
register.tag('paginate', do_paginate)
register.tag('autopaginate', do_autopaginate)

