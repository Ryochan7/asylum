from django.shortcuts import render

from mezzanine.core.views import direct_to_template
from mezzanine.pages.page_processors import processor_for 
from mezzanine.pages.models import Page

"""@processor_for("contact")
def contact_page(request, page):
    print "IN MINE"
    return render(request, "contact.html", {"page": page})
"""

