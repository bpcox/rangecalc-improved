from django import forms

class RangeForm(forms.Form):
    ranges = forms.CharField(widget=forms.Textarea(attrs={'cols': '41', 'rows': 20}))

