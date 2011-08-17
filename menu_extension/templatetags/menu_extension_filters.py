import re
from django import template
from django.core.urlresolvers import reverse

register = template.Library()

def check_path_lists (item_list, path_list):
    if len (item_list) > len (path_list):
        return False

    selected = False
    for i, part in enumerate (item_list):
        if part == path_list[i]:
            selected = True
        else:
            selected = False
            break

    return selected

def contains_url_path (url, path):
    full_url_list = path.replace ("/", " ").split ()
    url_list = url.replace ("/", " ").split ()

    return check_path_lists (url_list, full_url_list)

register.filter (contains_url_path)

def contains_named_path (named_url, path):
    full_url_list = path.replace ("/", " ").split ()
    named_url_list = reverse (named_url).replace ("/", " ").split ()

    return check_path_lists (named_url_list, full_url_list)

register.filter (contains_named_path)

