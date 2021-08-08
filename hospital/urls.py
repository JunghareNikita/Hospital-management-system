from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('admin', views.admin_signup),
    path('', views.home, name='home'),

    path('adminlogin/', LoginView.as_view(template_name='login.html'), name='adminlogin'),
    path('doctorlogin/', LoginView.as_view(template_name='login.html'), name='doctorlogin'),
    path('patientlogin/', LoginView.as_view(template_name='login.html'), name='patientlogin'),
    path('afterLogin/', views.afterLogin_view, name='afterLogin'),
    path('logout', LogoutView.as_view(template_name='home.html'), name='logout'),

    path('admin_signup/', views.admin_signup, name='admin_signup'),
    path('doctor_signup/', views.doctor_signup, name='doctor_signup'),
    path('patient_signup/', views.patient_signup, name='patient_signup'),

    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),

    path('admin_doctor', views.admin_doctor, name='admin_doctor'),
    path('admin_view_doctor', views.admin_view_doctor, name='admin_view_doctor'),
    path('admin_add_doctor', views.admin_add_doctor, name='admin_add_doctor'),
    path('admin_update_doctor/<int:pk>', views.admin_update_doctor, name='admin_update_doctor'),
    path('admin_delete_doctor/<int:pk>', views.admin_delete_doctor, name='admin_delete_doctor'),
    path('admin_approve_view', views.admin_approve_view, name='admin_approve_view'),
    path('admin_approve_doctor/<int:pk>', views.admin_approve_doctor, name='admin_approve_doctor'),
    path('admin_reject_doctor/<int:pk>', views.admin_reject_doctor, name='admin_reject_doctor'),
    path('admin_view_doctor_specialisation', views.admin_view_doctor_specialisation, name='admin_view_doctor_specialisation'),

    path('admin_patient_view', views.admin_patient_view, name='admin_patient_view'),
    path('admin_view_patient', views.admin_view_patient, name='admin_view_patient'),
    path('admin_add_patient', views.admin_add_patient, name='admin_add_patient'),
    path('admin_update_patient/<int:pk>', views.admin_update_patient, name='admin_update_patient'),
    path('admin_delete_patient/<int:pk>', views.admin_delete_patient, name='admin_delete_patient'),
    path('admin_approve_patient_view', views.admin_approve_patient_view, name='admin_approve_patient_view'),
    path('admin_approve_patient/<int:pk>', views.admin_approve_patient, name='admin_approve_patient'),
    path('admin_reject_patient/<int:pk>', views.admin_reject_patient, name='admin_reject_patient'),

    path('admin_appointment_view', views.admin_appointment_view, name='admin_appointment_view'),
    path('admin_view_appointment_view', views.admin_view_appointment_view, name='admin_view_appointment_view'),
    path('admin_book_appointment', views.admin_book_appointment, name='admin_book_appointment'),
    path('admin_approve_appointment_view', views.admin_approve_appointment_view, name='admin_approve_appointment_view'),
    path('admin_approve_appointment/<int:pk>', views.admin_approve_appointment, name='admin_approve_appointment'),
    path('admin_reject_appointment/<int:pk>', views.admin_reject_appointment, name='admin_reject_appointment'),

    path('admin_discharge_patient_view', views.admin_discharge_patient_view, name='admin_discharge_patient_view'),
    path('discharge_patient_view/<int:pk>', views.discharge_patient_view, name='discharge_patient_view'),
    path('patient_discharge_view', views.patient_discharge_view, name='patient_discharge_view'),

    path('doctor_dashboard', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor_patient_view', views.doctor_patient_view, name='doctor_patient_view'),
    path('doctor_view_patient', views.doctor_view_patient, name='doctor_view_patient'),
    path('doctor_appointment_view', views.doctor_appointment_view, name='doctor_appointment_view'),
    path('doctor_appointment_view', views.doctor_appointment_view, name='doctor_appointment_view'),
    path('doctor_view_appointment_view', views.doctor_view_appointment_view, name='doctor_view_appointment_view'),
    path('delete_appointment_view/<int:pk>', views.delete_appointment_view, name='delete_appointment_view'),
    path('doctor_delete_appointment_view', views.doctor_delete_appointment_view, name='doctor_delete_appointment_view'),
    path('doctor_discharge_patient_view', views.doctor_discharge_patient_view, name='doctor_discharge_patient_view'),

    path('patient_dashboard', views.patient_dashboard, name='patient_dashboard'),
    path('patient_appointment', views.patient_appointment, name='patient_appointment'),

]