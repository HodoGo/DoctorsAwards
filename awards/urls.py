from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.DoctorHome.as_view(), name='doctors'),
    path('doct/<int:pk>/', views.DoctorDetailView.as_view(), name='doctor-detail'),
]