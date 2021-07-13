from django import forms
from datetime import datetime
from .models import Lpu,Award
from bootstrap_datepicker_plus import DatePickerInput
from easy_select2.widgets import Select2
from bootstrap_datepicker_plus import DatePickerInput

class DoctorSearchForm(forms.Form):
    lastname = forms.CharField(required=False,label='Фамилия')

class DoctorReportForm(forms.Form):    
    incomDateB = forms.DateField(label='Дата вх. от',widget=forms.SelectDateWidget())
    incomDateE = forms.DateField(required=False,label='Дата вх. до',widget=forms.SelectDateWidget())
    #lpu = forms.ModelChoiceField(queryset=Lpu.objects.all(),widget=Select2())

class AwardSearchForm(forms.Form):
    start_date = forms.DateField(label='Дата вх. от',required=False,widget=DatePickerInput(format='%Y-%m-%d'))
    end_date = forms.DateField(required=False,label='Дата вх. до',widget=DatePickerInput(format='%Y-%m-%d'))
    export_to_xlsx_pivot = forms.BooleanField(required=False,label='Выгрузить сводный отчет')

