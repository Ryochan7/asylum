from django import forms
from contact_form.forms import AkismetContactForm, attrs_dict

class CustomContactForm (AkismetContactForm):
    body = forms.CharField(widget=forms.Textarea(attrs=attrs_dict),
                              label=u'Your message')

