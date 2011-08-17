import re
import logging
from urlparse import urlparse
from django import forms
from django.contrib.sites.models import Site
from treemenus.models import MenuItem

logger = logging.getLogger ("menu_extension.forms")

class MenuItemExtensionAdminForm (forms.ModelForm):
    class Meta (object):
        model = MenuItem

    def clean_url (self):
        current_site = None
        final_url = self.cleaned_data["url"]
        try:
            current_site = Site.objects.get_current ()
        except Site.DoesNotExist:
            current_site = None

        if current_site is None:
            return self.cleaned_data["url"]
        else:
            parsed_url = urlparse (self.cleaned_data["url"])
            if parsed_url.netloc == current_site.domain and (
                parsed_url.scheme == "http"):
                final_url = parsed_url.path
                
        return final_url

