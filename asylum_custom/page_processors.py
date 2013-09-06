from django.shortcuts import render
from django.template import RequestContext

from mezzanine.pages.page_processors import processor_for 
from mezzanine.forms.models import Form
from mezzanine.forms.signals import form_invalid, form_valid
from .forms import CustomContactForm

@processor_for(Form, "contact")
def contact_form(request, page):
    form = CustomContactForm(page.form, RequestContext(request),
        request.POST or None, request.FILES or None)
    
    # If form is invalid, interrupt any other page processing
    # and display errors found
    if not form.is_valid():
        form_invalid.send(sender=request, form=form)
        return render(request, "pages/contact.html", {"page": page, "form": form})

    return {}

