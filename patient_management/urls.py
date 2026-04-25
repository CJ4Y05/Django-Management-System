from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.home, name='home'),
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/create', views.patient_create, name='patient_create' ),
    path('patients/<int:patient_id>/edit/', views.patient_edit, name='patient_edit'),
    path('patients/<int:patient_id>/delete/', views.patient_delete, name='patient_delete'),
    path('addresses/', views.address_list, name='address_list'),
    path('addresses/create/', views.address_create, name='address_create'),
    path('addresses/<int:address_id>/edit/', views.address_edit, name='address_edit'),
    path('addresses/<int:address_id>/delete/', views.address_delete, name='address_delete'),
    path('emergencycontacts/', views.emergencycontact_list, name='emergencycontact_list'),
    path('emergencycontacts/create/', views.emergencycontact_create, name='emergencycontact_create'),
    path('emergencycontacts/<int:contact_id>/edit/', views.emergencycontact_edit, name='emergencycontact_edit'),
    path('emergencycontacts/<int:contact_id>/delete/', views.emergencycontact_delete, name='emergencycontact_delete'),
    path('guardians/', views.guardian_list, name='guardian_list'),
    path('guardians/create/', views.guardian_create, name='guardian_create'),
    path('guardians/<int:guardian_id>/edit/', views.guardian_edit, name='guardian_edit'),
    path('guardians/<int:guardian_id>/delete/', views.guardian_delete, name='guardian_delete'),
]