from django import forms

class DoctorSearchForm(forms.Form):
    lastname = forms.CharField(required=False,label='Фамилия')