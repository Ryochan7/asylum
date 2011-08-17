import re
from django import template
from django.core.urlresolvers import reverse

register = template.Library()

def check_path_lists (item_list, path_list):
    item_list_length = len (item_list)
    path_list_length = len (path_list)
    # Child can't be selected when parent is the active page
    if item_list_length > path_list_length:
        return False
    # Handle case of /
    elif item_list_length == path_list_length and item_list_length == 0:
        return True

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

