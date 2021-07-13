from django.db import models
from django.shortcuts import render, redirect
from django.views.generic import ListView,DetailView
from .models import Doctor,Award
from .forms import AwardSearchForm
import pandas as pd
from django.http import HttpResponse



#DataFlair
def index(request):
    return render(request, 'index.html')

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


def form_report(request):
    queryset = Award.objects.all()
    form = AwardSearchForm(request.POST or None)
    export_pivot = request.POST.get('export_to_xlsx_pivot', False)
    export_xlsx = request.POST.get('export_to_xlsx', False)
    if request.method == "POST":
        if(export_pivot):
            qs = Award.objects.filter(
                incoming_date__range=[
                    request.POST['start_date'], 
                    request.POST['end_date']]).values("doctor__lpu__name_lpu", "type_award__awardtype_name", "status")
            data = pd.DataFrame(qs)
            res = pd.pivot_table(data,index='doctor__lpu__name_lpu',columns='type_award__awardtype_name',values='status', aggfunc='count',margins=True, margins_name='Всего', fill_value=0)
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=your_template_name.xlsx'
            res.to_excel(response)
            return response
            
        if(request.POST['start_date'] and request.POST['end_date']):
            queryset = Award.objects.filter(            
                incoming_date__range=[
                    request.POST['start_date'],
                    request.POST['end_date']
                ]
            )


    context = {
        "queryset" : queryset,
        "form" : form
    }
    
    return render(request,'awards/search.html',context)
