from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.home, name='home'),
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/create', views.patient_create, name='patient_create' ),
    path('patients/<int:patient_id>/edit/', views.patient_edit, name='patient_edit'),
    path('patients/<int:patient_id>/delete/', views.patient_delete, name='patient_delete'),
]