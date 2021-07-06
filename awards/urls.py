from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.DoctorHome.as_view(), name='doctors'),
    path('doct/<int:pk>/', views.DoctorDetailView.as_view(), name='doctor-detail'),
    path('report/', views.all_report,name='all_report'),
    #path('/report/<int:year>/', views.year_report),
]