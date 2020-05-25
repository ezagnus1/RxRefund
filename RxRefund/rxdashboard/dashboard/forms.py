from django import forms



class dateforms(forms.Form):
    year_input = forms.IntegerField()
    month_input = forms.IntegerField()