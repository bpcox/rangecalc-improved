from django import forms

class RangeForm(forms.Form):
    ranges = forms.CharField(widget=forms.Textarea)
