from django import template
from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import InclusionTag

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
