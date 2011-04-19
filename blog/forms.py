from django import forms

class SearchForm (forms.Form):
    search = forms.CharField (max_length=100, widget=forms.TextInput (attrs={'size': '15'}))


