from django.db import models
from django.shortcuts import render, redirect
from django.views.generic import ListView,DetailView
from .models import Doctor,Award
import pandas as pd
from django.http import HttpResponse



#DataFlair
def index(request):
    shelf = Doctor.objects.all()
    return render(request, 'doctor/doc.html', {'shelf': shelf})

class DoctorHome(ListView):
    model = Doctor
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(lastname__icontains=query)
        else:
            object_list = self.model.objects.all()
        return object_list

class DoctorDetailView(DetailView):
    model = Doctor

def all_report(request):
    qs = Award.objects.filter(incoming_date__range=["2021-01-01", "2021-07-31"]).values("doctor__lpu__name_lpu", "type_award__awardtype_name", "status")
    data = pd.DataFrame(qs)
    res = pd.pivot_table(data,index='doctor__lpu__name_lpu',columns='type_award__awardtype_name',values='status', aggfunc='count',margins=True, margins_name='Всего', fill_value=0)
    return HttpResponse(res.to_html())


def year_report(request):
    pass
