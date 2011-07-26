from django import template
from addthis.conf import settings

register = template.Library()

@register.inclusion_tag ("addthis/addthis.html")
def addthis_share ():
    # Might use this later
    profile_id = settings.ADD_THIS_PROFILE_ID
    return {
        "profile_id": profile_id,
    }

@register.inclusion_tag ("addthis/addthis_header.html")
def addthis_header ():
    profile_id = settings.ADD_THIS_PROFILE_ID
    return {
        "profile_id": profile_id,
    }

