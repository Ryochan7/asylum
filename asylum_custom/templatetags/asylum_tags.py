from django import template
from classytags.core import Options, Tag
from classytags.arguments import Argument
from classytags.helpers import InclusionTag

from mezzanine.pages.models import Page

register = template.Library()

class BigDummy(InclusionTag):
    name = "bigdummy"
    template = "asylum/dummy.html"

    def get_context(self, context):
        return {"varname": "dummy"}

register.tag(BigDummy)

class CustomPaginationFor(InclusionTag):
    name = "custom_pagination_for"
    template = "includes/pagination.html"
    options = Options (
        Argument("current_page"),
        Argument("page_var", required=False, default="page"),
    )
    
    def get_context(self, context, current_page, page_var):
        querystring = context["request"].GET.copy()
        if page_var in querystring:
            del querystring[page_var]
        if "ajax" in querystring:
            del querystring["ajax"]

        querystring = querystring.urlencode()
        return {
            "current_page": current_page,
            "querystring": querystring,
            "page_var": page_var,
        }
    
register.tag(CustomPaginationFor)

class LoadForumsPage(Tag):
    name = "load_forums_page"

    def render_tag(self, context):
        possible_page = Page.objects.filter(slug="forums").first()
        if possible_page:
            context["page"] = possible_page

        return ''

register.tag(LoadForumsPage)
