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

