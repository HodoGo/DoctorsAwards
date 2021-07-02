from django.db import models
from django.shortcuts import render, redirect
from django.views.generic import ListView,DetailView
from .models import Doctor
#from .forms import BookCreate
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
