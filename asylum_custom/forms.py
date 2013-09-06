from django import forms

from mezzanine.forms.forms import FormForForm

class CustomContactForm(FormForForm):
    def clean_field_1(self):
        name = self.cleaned_data["field_1"]
        if not name.strip():
            raise forms.ValidationError("Please include a name")

        return name

    def clean_field_4(self):
        message = self.cleaned_data["field_4"]
        if not message.strip():
            raise forms.ValidationError("Please specify a message")

        return message

