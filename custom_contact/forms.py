from django import forms
from contact_form.forms import ContactForm, AkismetContactForm, attrs_dict

class CustomContactForm (ContactForm):
    body = forms.CharField(widget=forms.Textarea(attrs=attrs_dict),
                              label=u'Your message')

